This is a flask application for sportsbook product which is responsible for managing sports, events and selections.
Currently, the app has no good UI, only a layout template for it.

## Running the application locally

### Package Download Manager -
To download libraries, [pip](https://pip.pypa.io/en/stable/) has been used and is advised. 
Make sure it is installed.

## Create Virtual Environment

This is a Python script and to install all the related libraries, it is advised to first create a virtual environment.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install [virtualenv](https://pypi.org/project/virtualenv/).

```bash
pip install virtualenv
```

Check how to setup virtual environment from here - https://virtualenv.pypa.io/en/latest/user_guide.html


## Requirements
All the libraries along with their versions are mentioned in the file requirements.txt.


Use the command pip install -r requirements.txt in your terminal. This will install all the packages listed in your requirements. txt file.

```bash
pip install -r requirements.txt
```

## Usage
To run the flask application, follow these steps:

1. Ensure you have Python installed on your system.
2. Create a .env file in the root directory of the project and define the following environment variables:
   ```python
    MYSQL_DATABASE_HOST="localhost"
    MYSQL_DATABASE_USER='root'
    MYSQL_DATABASE_PASSWORD='password'
    MYSQL_MASTER_SCHEMA='dev'
    ```
3. build and run Docker containers
    docker-compose up --build
### To Initialize the Database
    ```bash
    docker exec -it sportspro_app python sportspro/db/init_db.py
    ```
    This command is not required to run, as db is initialized in test cases

### To run test cases - 
```python
pytest .\sportspro\tests
  ```
