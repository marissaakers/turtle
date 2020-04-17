import os

def get_env_variable(name):
	try:
		return os.environ.get(name)
	except KeyError:
		message = "Expected environment variable '{}' not set." . format(name)
		raise Exception(message)

def create_db_url(user, pw, url, db):
	return f"postgresql://{user}:{pw}@{url}/{db}"

# Database secrets
POSTGRES_USER='MTRG_ADMIN'
POSTGRES_PW='qR)SMn^w8LKxb4^iq^L2'
POSTGRES_URL='turtledb2.cryuatlylxd4.us-east-1.rds.amazonaws.com'
POSTGRES_DB='postgres'

DB_URL = create_db_url(POSTGRES_USER, POSTGRES_PW, POSTGRES_URL, POSTGRES_DB)

class Config(object):
	SQLALCHEMY_DATABASE_URI = DB_URL
	SQLALCHEMY_TRACK_MODIFICATIONS = False