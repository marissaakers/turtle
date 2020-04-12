# MTRG Backend
The backend uses Python scripts run on AWS Lambda to interact with the PotsgreSQL database hosted on AWS RDS, as well as static files hosted on S3. The scripts are activated when a call to AWS API Gateway is made, usually when a JSON is POSTed.

# Contents
The base folder contains various files for first-time setup of the project, as well as configuration files.

`requirements.txt` contains a list of python modules necessary to run the backend. In a Python 3.7 virtual environment, run `pip install -r requirements.txt` to install them.

`turtle.sh` sets environment variables, and begins running the API locally

`migration.py` is a script to migrate information from the old filemaker database in CSV format to the new database
### migrations
Automatically generated folder used by Alembic for managing database versions. For example, when an integer column is added to the database.

### turtleapi
Python files that make up the backend
