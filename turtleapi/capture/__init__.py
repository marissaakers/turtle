from flask import Blueprint, request
from flask_restful import Resource, Api
#from turtleapi.models.turtlemodels import Clutch, ClutchSchema
from turtleapi.models.turtlemodels import LagoonEncounterSchema
import json
from turtleapi.capture.query_lagoon import query_lagoon
from turtleapi.capture.insert_lagoon import insert_lagoon

capturebp = Blueprint('captureapi', __name__)
api = Api(capturebp)

turtles = {
	'1': 'leatherback',
	'2': 'loggerhead'
}

class Lagoon(Resource):
	def get(self):
		return query_lagoon(), 200

	def post(self):
		json_data = request.get_json(force=True)
		return insert_lagoon(json_data), 200

	# def get(self):
	# 	clutches = Clutch.query.all()
	# 	clutches_schema = ClutchSchema(many=True)
	# 	output = clutches_schema.dump(clutches)
	# 	return output, 200

	# def post(self):
	# 	json_data = request.get_json(force=True)
	# 	return json_data, 200

	# def put(self):
	# 	json_data = request.get_json(force=True)
	# 	for key, value in json_data.items():
	# 		turtles[key] = value
	# 	return turtles, 200

	# def delete(self):
	# 	args = request.args
	# 	turtle_id = args['id']
	# 	del turtles[turtle_id]
	# 	return turtles, 204

api.add_resource(Lagoon, '/api/capture/lagoon')

