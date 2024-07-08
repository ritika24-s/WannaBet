import os
import traceback
import mysql.connector
from mysql.connector import Error, errorcode

from ..config import config_by_name
from ..utils.logger import setup_logger
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__name__))
load_dotenv(os.path.join(basedir, '.env'))
config = config_by_name[os.getenv('FLASK_ENV', 'development')]
logger = setup_logger("main_db", os.getenv('FLASK_ENV', 'development'))

class DB(object):
    def __init__(self):
        self.config = config
        # self._sql_db = None
        self.connect()


    def connect(self):
        try:
            self._sql_db = mysql.connector.connect(
                host=self.config.MYSQL_DATABASE_HOST,
                user=self.config.MYSQL_DATABASE_USER,
                password=self.config.MYSQL_DATABASE_PASSWORD,
                database=self.config.MYSQL_MASTER_SCHEMA,
                autocommit=True
                # ssl_verify_identity=self.config.SSL_VERIFY_IDENTITY
            )
            
        except mysql.connector.Error as err:
            logger.error(f"Error connecting to the database: {err}")

    # function to close the db connection
    def close(self):
        """
        This function closes the current db connection by calling the close function of mysql connection
        :return: None
        """
        if self._sql_db and self._sql_db.is_connected():
            self._sql_db.close()

    # function to close the cursor
    def close_cursor(self, cursor):
        """
        This function is used to close the cursor after the cursor is no longer in use
        :param cursor: cursor parameter
        :return: None
        """
        try:
            # try to close the cursor if it exists
            if cursor:
                cursor.close()

        except mysql.connector.errors.InternalError as ie:
            # In case of Unread result found exception, fetch all the results of the cursor,
            # that will reset the cursor and then try to close again
            cursor.fetchall()
        except mysql.connector.Error as e:
            # reconnect the connection and that will solve all the other errors that might occur
            self.reconnect()
        finally:
            # finally close the cursor
            cursor.close()

    def reconnect(self):
        try:
            if not self._sql_db:
                self.connect()
            if not self._sql_db.is_connected():
                self._sql_db.reconnect()
        except mysql.connector.Error as err:
            setup_logger(err)

    # this function is used to fetch data from any table of mysql with where clause
    def select_data_where(self, select, table, where, fetchone=True):
        """
        This function is used to create select where query and fetch results

        Note: This function is not used for combining where conditions, only one condition can be used

        :param select: str of columns needed
        :param table: name of the table
        :param where: where conditions that needs to be fulfilled
        :param fetchone: if only one row is required or should fetchall be performed
        :return: returns the results
        """
        results = []
        cursor = None

        try:
            self.reconnect()
            cursor = self._sql_db.cursor()

            if fetchone:
                # if only fetching one entry, then limit the data to 1 to optimize the query return
                cursor.execute(f"select {select} from {table} where {where} LIMIT 1;")
                results = [cursor.fetchone()]
            else:
                cursor.execute(f"select {select} from {table} where {where};")
                results = cursor.fetchall()
        except mysql.connector.Error as err:
            setup_logger("Got an error while connecting to the MySQL database -" + str(err))
            traceback.print_exc()
        finally:
            # close the cursor and connection
            self.close_cursor(cursor)
            self.close()
            return results

    def execute_query(self, query, values=None, insert=False):
        """
        This function will handle all the insert, update and delete queries
        """
        results = None
        cursor = None

        try:
            self.reconnect()
            cursor = self._sql_db.cursor()
            cursor.execute(query, values)
                   
            if insert:
                results = cursor.lastrowid
            else:
                results = cursor.rowcount
            
            self._sql_db.commit()

        except mysql.connector.Error as err:
            self._sql_db.rollback()
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                setup_logger("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                setup_logger("Database does not exist")
            else:
                setup_logger("Got an error while connecting to the MySQL database -" + str(err))
            traceback.print_exc()
        finally:
            # close the cursor and connection
            self.close_cursor(cursor)
            self.close()
            return results

