from flask import Blueprint, request
from flask_restful import Resource, Api
from flask_restful.utils import cors
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

class InsertLagoon(Resource):
	@cors.crossdomain(origin='*')

	def post(self):
		json_data = request.get_json(force=True)
		return insert_lagoon(json_data), 200
		# insert_lagoon()
		# return 200

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

class QueryLagoon(Resource):
	@cors.crossdomain(origin='*')
	# def get(self):
	# 	return query_lagoon(), 200

	def post(self):
		json_data = request.get_json(force=True)
		return query_lagoon(json_data), 200



api.add_resource(InsertLagoon, '/api/capture/lagoon/insert')
api.add_resource(QueryLagoon, '/api/capture/lagoon/query')

