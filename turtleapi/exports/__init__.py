from flask import Blueprint, request
from turtleapi.capture.lagoon import query_lagoon
from turtleapi.exports.csv_exports import csv_export, field_lister
from turtleapi.exports.survey_csv_exports import survey_csv_export, survey_field_lister
from turtleapi.exports.filters import save_filters, list_filters, get_filters, delete_filters
from turtleapi.exports.survey_filters import (save_survey_filters, list_survey_filters, 
    get_survey_filters, delete_survey_filters)

exportsbp = Blueprint('exports', __name__, url_prefix='/api/exports')

@exportsbp.route('/csv', methods=['GET', 'POST'])
def post():
    # Grab the JSON coming in
    json_data = request.get_json(force=True)

    # Return csv of query
    return csv_export(json_data)

@exportsbp.route('/fields/capture', methods=['GET'])
def get_capture_fields():
    # # Grab the JSON coming in
    # json_data = request.get_json(force=True)

    # Return list of available tables & fields
    return field_lister()

@exportsbp.route('/filters/get-by-username', methods=['POST'])
def get_filter_sets_by_username():
    json_data = request.get_json(force=True)
    return list_filters(json_data['username'])

@exportsbp.route('/filters/get', methods=['POST'])
def get_filter_set_by_id():
    json_data = request.get_json(force=True)
    return get_filters(json_data['filter_set_id'])

@exportsbp.route('/filters/save', methods=['POST'])
def save_filter_set():
    json_data = request.get_json(force=True)
    return save_filters(json_data)

@exportsbp.route('/filters/delete/<int:filter_set_id>', methods=['DELETE'])
def delete_filter_set(filter_set_id):
    return delete_filters(filter_set_id)

@exportsbp.route('/csv/survey', methods=['GET', 'POST'])
def postsurvey():
    # Grab the JSON coming in
    json_data = request.get_json(force=True)

    # Return csv of query
    return survey_csv_export(json_data)

@exportsbp.route('/fields/survey', methods=['GET'])
def get_survey_fields():
    # # Grab the JSON coming in
    # json_data = request.get_json(force=True)

    # Return list of available tables & fields
    return survey_field_lister()

@exportsbp.route('/surveyfilters/get-by-username', methods=['POST'])
def get_survey_filter_sets_by_username():
    json_data = request.get_json(force=True)
    return list_survey_filters(json_data['username'])

@exportsbp.route('/surveyfilters/get', methods=['POST'])
def get_survey_filter_set_by_id():
    json_data = request.get_json(force=True)
    return get_survey_filters(json_data['filter_set_id'])

@exportsbp.route('/surveyfilters/save', methods=['POST'])
def save_survey_filter_set():
    json_data = request.get_json(force=True)
    return save_survey_filters(json_data)

@exportsbp.route('/filters/delete/<int:filter_set_id>', methods=['DELETE'])
def delete_survey_filter_set(filter_set_id):
    return delete_survey_filters(filter_set_id)