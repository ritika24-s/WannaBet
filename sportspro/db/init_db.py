import mysql.connector
from mysql.connector import errorcode

from sportspro.db import DB

class CreateSchema(DB):
    """
    This class is only to be run manually by admin or during test runs
    """
    # def __init__(self):
    #     super().__init__()

    def del_db(self):
        """
        Function to delete databases. Only for testing purposes.
        Please dont call from anywhere else.
        """
        self.execute_query("DROP TABLE selections; DROP TABLE events; DROP TABLE sports;")

    def init_db(self):
        self.reconnect()
        cursor = self._sql_db.cursor()

        # Load schemas.sql
        with open('sportspro/db/schemas.sql', 'r') as f:
            schema_sql = f.read()

        # Execute schema.sql
        try:
            for result in cursor.execute(schema_sql, multi=True):
                pass
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table already exists.")
            else:
                print(err.msg)
        else:
            print("Database initialized successfully.")

        self.close_cursor(cursor)
        self.close()

if __name__ == "__main__":
    create_schema = CreateSchema()
    create_schema.init_db()
