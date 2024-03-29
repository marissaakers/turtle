from flask import Blueprint, request, render_template
import requests
import json
from turtleapi.reports.reports import lagoon_report
from turtleapi.capture.lagoon import query_lagoon

reportsbp = Blueprint('reports', __name__, url_prefix='/api/reports')

@reportsbp.route('/lagoon/pdf', methods=['GET','POST'])
def post():
    # Grab the JSON coming in
    json_data = request.get_json(force=True)

    # Use the filters to get our data via query_lagoon
    query_data = query_lagoon(json_data['filters'])

    # Now generate a report based on those filters
    return lagoon_report(query_data, json_data['features'], json_data['report_info'])