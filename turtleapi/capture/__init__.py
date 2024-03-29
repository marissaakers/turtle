from flask import Blueprint, request, jsonify, Response
from flask_restful import Resource, Api
import json
from turtleapi.capture.lagoon import (mini_query_lagoon, query_lagoon, query_lagoon_metadata, insert_lagoon,
	insert_lagoon_metadata, edit_lagoon, edit_lagoon_metadata, delete_lagoon, delete_lagoon_metadata)
from turtleapi.capture.trident import (mini_query_trident, query_trident, query_trident_metadata, insert_trident,
	insert_trident_metadata, edit_trident, edit_trident_metadata, delete_trident, delete_trident_metadata)
from turtleapi.capture.beach import mini_query_beach, query_beach, insert_beach, edit_beach, delete_beach
from turtleapi.capture.offshore import (mini_query_offshore, query_offshore, insert_offshore, edit_offshore,
	delete_offshore)
from turtleapi.capture.sample_tracking import (get_sample, update_sample, add_sample, delete_sample, 
add_tracking_entry, update_tracking_entry, delete_tracking_entry)
from turtleapi.capture.util import get_file, put_file, return_tag_status

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

class DeleteLagoonMetadata(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		response = delete_lagoon_metadata(json_data)
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

class QueryTrident(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		return query_trident(json_data)

class QueryTridentMetadata(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		return query_trident_metadata(json_data)

class EditTrident(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		response = edit_trident(json_data)
		return response, 200

class DeleteTrident(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		response = delete_trident(json_data)
		return response, 200

class EditTridentMetadata(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		response = edit_trident_metadata(json_data)
		return response, 200

class DeleteTridentMetadata(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		response = delete_trident_metadata(json_data)
		return response, 200

class InsertOffshore(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		response = insert_offshore(json_data)
		return response, 200

class MiniQueryOffshore(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		return mini_query_offshore(json_data)

class QueryOffshore(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		return query_offshore(json_data)

class EditOffshore(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		response = edit_offshore(json_data)
		return response, 200

class DeleteOffshore(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		response = delete_offshore(json_data)
		return response, 200

class MiniQueryBeach(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		return mini_query_beach(json_data)

class QueryBeach(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		return query_beach(json_data)

class InsertBeach(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		response = insert_beach(json_data)
		return response, 200

class EditBeach(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		response = edit_beach(json_data)
		return response, 200

class DeleteBeach(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		response = delete_beach(json_data)
		return response, 200

class GetFile(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		response = get_file(json_data)
		return response

class PutFile(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		response = put_file(json_data)
		return response

class Sample(Resource):
	def get(self, sample_id):
		# We get a sample id, and send back sample info including tracking
		response = get_sample(sample_id)
		return response, 200

	def post(self):
		sample = request.get_json(force=True)
		response = add_sample(sample)
		return response, 201

	def put(self):
		json_data = request.get_json(force=True)
		response = update_sample(json_data)
		return response, 200

	def delete(self, sample_id):
		response = delete_sample(sample_id)
		return response, 200
class SampleTracking(Resource):

	def post(self):
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

class TagStatus(Resource):
	def post(self):
		tags = request.get_json(force=True)
		return return_tag_status(tags), 200

api.add_resource(MiniQueryLagoon, '/api/capture/lagoon/mini_query')
api.add_resource(QueryLagoon, '/api/capture/lagoon/query')
api.add_resource(InsertLagoon, '/api/capture/lagoon/insert')
api.add_resource(EditLagoon, '/api/capture/lagoon/edit')
api.add_resource(DeleteLagoon, '/api/capture/lagoon/delete')
api.add_resource(InsertLagoonMetadata, '/api/capture/lagoon/metadata/insert')
api.add_resource(QueryLagoonMetadata, '/api/capture/lagoon/metadata/query')
api.add_resource(EditLagoonMetadata, '/api/capture/lagoon/metadata/edit')
api.add_resource(DeleteLagoonMetadata, '/api/capture/lagoon/metadata/delete')

api.add_resource(MiniQueryTrident, '/api/capture/trident/mini_query')
api.add_resource(QueryTrident, '/api/capture/trident/query')
api.add_resource(InsertTrident, '/api/capture/trident/insert')
api.add_resource(EditTrident, '/api/capture/trident/edit')
api.add_resource(DeleteTrident, '/api/capture/trident/delete')
api.add_resource(InsertTridentMetadata, '/api/capture/trident/metadata/insert')
api.add_resource(QueryTridentMetadata, '/api/capture/trident/metadata/query')
api.add_resource(EditTridentMetadata, '/api/capture/trident/metadata/edit')
api.add_resource(DeleteTridentMetadata, '/api/capture/trident/metadata/delete')

api.add_resource(MiniQueryOffshore, '/api/capture/offshore/mini_query')
api.add_resource(QueryOffshore, '/api/capture/offshore/query')
api.add_resource(InsertOffshore, '/api/capture/offshore/insert')
api.add_resource(EditOffshore, '/api/capture/offshore/edit')
api.add_resource(DeleteOffshore, '/api/capture/offshore/delete')

api.add_resource(MiniQueryBeach, '/api/capture/beach/mini_query')
api.add_resource(QueryBeach, '/api/capture/beach/query')
api.add_resource(InsertBeach, '/api/capture/beach/insert')
api.add_resource(EditBeach, '/api/capture/beach/edit')
api.add_resource(DeleteBeach, '/api/capture/beach/delete')

api.add_resource(GetFile, '/api/capture/file/get')
api.add_resource(PutFile, '/api/capture/file/put')

api.add_resource(Sample, '/api/capture/sample', '/api/capture/sample/<int:sample_id>')
api.add_resource(SampleTracking, '/api/capture/sample/tracking',
								'/api/capture/sample/tracking/<int:sample_tracking_id>')

api.add_resource(TagStatus, '/api/capture/tagstatus')