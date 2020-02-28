from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from turtleapi.config import Config
from sqlathanor import FlaskBaseModel, initialize_flask_sqlathanor

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
#api = Api()

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(config_class)

	CORS(app)
	db = SQLAlchemy(app, model_class=FlaskBaseModel)
	db = initialize_flask_sqlathanor(db)
	migrate.init_app(app, db)
	#api = Api(app)

	register_blueprints(app)

	from turtleapi.models import turtlemodels

	return app

def register_blueprints(app):
	from turtleapi.capture import capturebp
	from turtleapi.reports import reportsbp
	from turtleapi.exports import exportsbp
	app.register_blueprint(capturebp)
	app.register_blueprint(reportsbp)
	app.register_blueprint(exportsbp)