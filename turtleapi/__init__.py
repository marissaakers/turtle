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
app = Flask(__name__)

def create_app(config_class=Config):
	app.config.from_object(config_class)

	register_blueprints(app)

	CORS(app)
	db = SQLAlchemy(app, model_class=FlaskBaseModel)
	db = initialize_flask_sqlathanor(db)
	migrate.init_app(app, db)

	app.config.update(
		ACCESS_KEY_ID='AKIAVA5HZOYYIC335DWA',
		SECRET_ACCESS_KEY='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',
		S3_BUCKET='mtrg-files-bucket'
	)

	from turtleapi.models import turtlemodels

	return app

def register_blueprints(app):
	from turtleapi.capture import capturebp
	from turtleapi.reports import reportsbp
	from turtleapi.survey import surveybp
	from turtleapi.exports import exportsbp
	app.register_blueprint(capturebp)
	app.register_blueprint(reportsbp)
	app.register_blueprint(surveybp)
	app.register_blueprint(exportsbp)