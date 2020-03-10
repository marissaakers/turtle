from flask import Blueprint, request
from turtleapi.capture.lagoon import query_lagoon
from turtleapi.exports.csv_exports import lagoon_csv_export

exportsbp = Blueprint('exports', __name__, url_prefix='/api/exports')

@exportsbp.route('/lagoon/csv', methods=['GET', 'POST'])
def post():
    # Grab the JSON coming in
    json_data = request.get_json(force=True)

    # Use the filters to get our data via query_lagoon
    query_data = query_lagoon(json_data['filters'])

    # Now call the method we need
    return lagoon_csv_export(query_data, json_data['features'])