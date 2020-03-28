from flask import Blueprint, request
from turtleapi.capture.lagoon import query_lagoon
from turtleapi.exports.csv_exports import csv_export

exportsbp = Blueprint('exports', __name__, url_prefix='/api/exports')

@exportsbp.route('/csv', methods=['GET', 'POST'])
def post():
    # Grab the JSON coming in
    json_data = request.get_json(force=True)

    # Return csv of query
    return csv_export(json_data)

def get():
    # Return list of available tables & fields
    return field_lister()