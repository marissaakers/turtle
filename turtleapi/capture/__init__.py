from flask import Blueprint, request
from flask_restful import Resource, Api
from turtleapi.models.turtlemodels import Clutch, ClutchSchema
import json

capturebp = Blueprint('captureapi', __name__)
api = Api(capturebp)

turtles = {
	'1': 'leatherback',
	'2': 'loggerhead'
}

class HelloWorld(Resource):
	def get(self):
		clutches = Clutch.query.all()
		clutches_schema = ClutchSchema(many=True)
		output = clutches_schema.dump(clutches)
		return output, 200

	def post(self):
		json_data = request.get_json(force=True)
		return json_data, 200

	def put(self):
		json_data = request.get_json(force=True)
		for key, value in json_data.items():
			turtles[key] = value
		return turtles, 200

	def delete(self):
		args = request.args
		turtle_id = args['id']
		del turtles[turtle_id]
		return turtles, 204

api.add_resource(HelloWorld, '/hello')

