from flask import Blueprint, request, jsonify, Response
from flask_restful import Resource, Api
import json
from turtleapi.capture.lagoon import query_lagoon, mini_query_lagoon, insert_lagoon, edit_lagoon, delete_lagoon
from turtleapi.capture.trident import (mini_query_trident, insert_trident, query_trident_metadata,
	insert_trident_metadata)
from turtleapi.capture.beach import insert_beach
from turtleapi.capture.metadata import (query_lagoon_metadata, insert_lagoon_metadata,
	query_offshore_metadata, insert_offshore_metadata, edit_lagoon_metadata)
# from turtleapi.capture.sample_tracking import (get_sample, add_tracking_entry,
# 	update_tracking_entry, delete_tracking_entry)

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

class InsertLagoonMetadata(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		response = insert_lagoon_metadata(json_data)
		return response, 200

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

class MiniQueryLagoon(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		return mini_query_lagoon(json_data)

class QueryLagoon(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		return query_lagoon(json_data)

class QueryLagoonMetadata(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		return query_lagoon_metadata(json_data)

class EditLagoon(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		response = edit_lagoon(json_data)
		return response, 200

class DeleteLagoon(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		response = delete_lagoon(json_data)
		return response, 200

class EditLagoonMetadata(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		response = edit_lagoon_metadata(json_data)
		return response, 200

class InsertTrident(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		response = insert_trident(json_data)
		return response, 200
		# insert_trident()
		# return 200

class InsertTridentMetadata(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		response = insert_trident_metadata(json_data)
		return response, 200

class MiniQueryTrident(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		return mini_query_trident(json_data)
# class QueryTrident(Resource):

class QueryTridentMetadata(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		return query_trident_metadata(json_data)

# class EditTrident(Resource):
# class InsertOffshore(Resource):

class InsertOffshoreMetadata(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		response = insert_offshore_metadata(json_data)
		return response, 200

# class MiniQueryOffshore(Resource):
# class QueryOffshore(Resource):

class QueryOffshoreMetadata(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		return query_offshore_metadata(json_data)

# class EditOffshore(Resource):

class InsertBeach(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		response = insert_beach(json_data)
		return response, 200

# class MiniQueryBeach(Resource):
# class QueryBeach(Resource):
# class EditBeach(Resource):

# class Sample(Resource):
# 	def get(self, sample_id):
# 		# We get a sample id, and send back sample info including tracking
# 		response = get_sample(sample_id)
# 		return response, 200

# class SampleTracking(Resource):

# 	def post(self):
# 		print(request.get_json(force=True))
# 		tracking_entry = request.get_json(force=True)
# 		response = add_tracking_entry(tracking_entry)
# 		return response, 201

# 	def put(self, sample_tracking_id):
# 		tracking_entry = request.get_json(force=True)
# 		response = update_tracking_entry(sample_tracking_id, tracking_entry)
# 		return response, 200

# 	def delete(self, sample_tracking_id):
# 		response = delete_tracking_entry(sample_tracking_id)
# 		return response, 200

api.add_resource(MiniQueryLagoon, '/api/capture/lagoon/mini_query')
api.add_resource(QueryLagoon, '/api/capture/lagoon/query')
api.add_resource(InsertLagoon, '/api/capture/lagoon/insert')
api.add_resource(EditLagoon, '/api/capture/lagoon/edit')
api.add_resource(DeleteLagoon, '/api/capture/lagoon/delete')
api.add_resource(InsertLagoonMetadata, '/api/capture/lagoon/metadata/insert')
api.add_resource(QueryLagoonMetadata, '/api/capture/lagoon/metadata/query')
api.add_resource(EditLagoonMetadata, '/api/capture/lagoon/metadata/edit')

api.add_resource(InsertTrident, '/api/capture/trident/insert')
api.add_resource(InsertTridentMetadata, '/api/capture/trident/metadata/insert')
api.add_resource(MiniQueryTrident, '/api/capture/trident/mini_query')
# api.add_resource(QueryTrident, '/api/capture/trident/query')
api.add_resource(QueryTridentMetadata, '/api/capture/trident/metadata/query')
# api.add_resource(EditTrident, '/api/capture/trident/edit')

# api.add_resource(InsertOffshore, '/api/capture/offshore/insert')
api.add_resource(InsertOffshoreMetadata, '/api/capture/offshore/metadata/insert')
# api.add_resource(MiniQueryOffshore, '/api/capture/offshore/mini_query')
# api.add_resource(QueryOffshore, '/api/capture/offshore/query')
api.add_resource(QueryOffshoreMetadata, '/api/capture/offshore/metadata/query')
# api.add_resource(EditOffshore, '/api/capture/offshore/edit')

api.add_resource(InsertBeach, '/api/capture/beach/insert')
# api.add_resource(MiniQueryBeach, '/api/capture/beach/mini_query')
# api.add_resource(QueryBeach, '/api/capture/beach/query')
# api.add_resource(EditBeach, '/api/capture/beach/edit')

# api.add_resource(Sample, '/api/capture/sample/<int:sample_id>')
# api.add_resource(SampleTracking, '/api/capture/sample/tracking',
# 								'/api/capture/sample/tracking/<int:sample_tracking_id>')
