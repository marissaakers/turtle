from flask import Blueprint, request, jsonify, Response
from flask_restful import Resource, Api
import json
from turtleapi.survey.bigsurvey import (insert_pafb, insert_mid_reach, insert_south_reach)
from turtleapi.survey.falsecrawl import (get_false_crawls, add_false_crawl, update_false_crawl,
    delete_false_crawl)
from turtleapi.survey.depredation import (get_depredations, add_depredation, update_depredation,
    delete_depredation)
from turtleapi.survey.scarp import (get_scarps, add_scarp, update_scarp, delete_scarp)

surveybp = Blueprint('surveyapi', __name__)
api = Api(surveybp)

class InsertPAFB(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        return insert_pafb(json_data)

class InsertMidReach(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        return insert_mid_reach(json_data)

class InsertSouthReach(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        return insert_south_reach(json_data)

class FalseCrawl(Resource):
    def get(self):
        response = get_false_crawls()
        if response is not None:
            return response, 200
        else:
            return 500
    
    def post(self):
        json_data = request.get_json(force=True)
        response = add_false_crawl(json_data)
        if response is not None:
            return response, 200
        else:
            return 500

    def put(self):
        json_data = request.get_json(force=True)
        return update_false_crawl(json_data)

    def delete(self, false_crawl_id):
        response = delete_false_crawl(false_crawl_id)
        return response, 200 if response else 500

class Depredation(Resource):
    def get(self):
        response = get_depredations()
        if response is not None:
            return response, 200
        else:
            return 500
    
    def post(self):
        json_data = request.get_json(force=True)
        response = add_depredation(json_data)
        if response is not None:
            return response, 200
        else:
            return 500

    def put(self):
        json_data = request.get_json(force=True)
        return update_depredation(json_data)

    def delete(self, depredation_id):
        response = delete_depredation(depredation_id)
        return response, 200 if response else 500

class Scarp(Resource):
    def get(self):
        response = get_scarps()
        if response is not None:
            return response, 200
        else:
            return 500
    
    def post(self):
        json_data = request.get_json(force=True)
        response = add_scarp(json_data)
        if response is not None:
            return response, 200
        else:
            return 500

    def put(self):
        json_data = request.get_json(force=True)
        return update_scarp(json_data)

    def delete(self, scarp_id):
        response = delete_scarp(scarp_id)
        return response, 200 if response else 500

api.add_resource(InsertPAFB, '/api/survey/pafb/insert')
api.add_resource(InsertMidReach, '/api/survey/mid/insert')
api.add_resource(InsertSouthReach, '/api/survey/south/insert')
api.add_resource(FalseCrawl, '/api/survey/falsecrawl', '/api/survey/falsecrawl/<int:false_crawl_id>')
api.add_resource(Depredation, '/api/survey/depredation', '/api/survey/depredation/<int:depredation_id>')
api.add_resource(Scarp, '/api/survey/scarp', '/api/survey/scarp/<int:scarp_id>')