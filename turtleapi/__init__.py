from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from turtleapi.config import Config

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
#api = Api()

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(config_class)

	db.init_app(app)
	ma.init_app(app)
	migrate.init_app(app, db)
	#api = Api(app)

	register_blueprints(app)

	from turtleapi.models import turtlemodels

	return app

def register_blueprints(app):
	from turtleapi.capture import capturebp
	app.register_blueprint(capturebp)