from flask import Blueprint, request
from flask_restful import Resource, Api
#from turtleapi.models.turtlemodels import Clutch, ClutchSchema
from turtleapi.models.turtlemodels import LagoonEncounterSchema
import json
from turtleapi.capture.query_lagoon import query_lagoon
from turtleapi.capture.insert_lagoon import insert_lagoon
from turtleapi.capture.edit_lagoon import edit_lagoon
from turtleapi.capture.insert_trident import insert_trident
from turtleapi.capture.metadata import query_metadata, insert_metadata
from turtleapi.capture.sample_tracking import (get_sample, add_tracking_entry,
	update_tracking_entry, delete_tracking_entry)

capturebp = Blueprint('captureapi', __name__)
api = Api(capturebp)

turtles = {
	'1': 'leatherback',
	'2': 'loggerhead'
}

class InsertLagoon(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		response = insert_lagoon(json_data)
		return response, 200
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
	def post(self):
		json_data = request.get_json(force=True)
		response = query_lagoon(json_data)
		return response, 200

class EditLagoon(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		response = edit_lagoon(json_data)
		return response, 200

class InsertTrident(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		response = insert_trident(json_data)
		return response, 200
		# insert_trident()
		# return 200

class QueryMetadata(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		response = query_metadata(json_data)
		return response, 200

class InsertMetadata(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		response = insert_metadata(json_data)
		return response, 200

class Sample(Resource):
	def get(self, sample_id):
		# We get a sample id, and send back sample info including tracking
		response = get_sample(sample_id)
		return response, 200

class SampleTracking(Resource):

	def post(self):
		print(request.get_json(force=True))
		tracking_entry = request.get_json(force=True)
		response = add_tracking_entry(tracking_entry)
		return response, 201

	def put(self, sample_tracking_id):
		tracking_entry = request.get_json(force=True)
		response = update_tracking_entry(sample_tracking_id, tracking_entry)
		return response, 200

	def delete(self, sample_tracking_id):
		response = delete_tracking_entry(sample_tracking_id)
		return response, 200

api.add_resource(InsertLagoon, '/api/capture/lagoon/insert')
api.add_resource(QueryLagoon, '/api/capture/lagoon/query')
api.add_resource(EditLagoon, '/api/capture/lagoon/edit')
api.add_resource(InsertTrident, '/api/capture/trident/insert')
api.add_resource(QueryMetadata, '/api/capture/metadata/query')
api.add_resource(InsertMetadata, '/api/capture/metadata/insert')
api.add_resource(Sample, '/api/capture/sample/<int:sample_id>')
api.add_resource(SampleTracking, '/api/capture/sample/tracking',
								'/api/capture/sample/tracking/<int:sample_tracking_id>')
