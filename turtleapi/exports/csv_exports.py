from flask import request, make_response
import csv
from io import StringIO
from turtleapi.models.turtlemodels import (LagoonEncounter, TridentEncounter, Encounter, Turtle, Tag,
                                           Morphometrics, Sample, Metadata, LagoonMetadata, Net,
                                           IncidentalCapture, BeachEncounter, OffshoreEncounter,
                                           OffshoreMetadata, TridentMetadata, SampleTracking, Clutch)
from turtleapi import db
from sqlalchemy.orm import load_only
from sqlalchemy import select
import datetime
from collections import OrderedDict

# from sqlalchemy.orm import with_polymorphic
# from turtleapi.models.turtlemodels import Turtle, Tag, Encounter, LagoonEncounter, TridentEncounter, BeachEncounter, OffshoreEncounter
# import json
# from flask import jsonify, make_response, redirect, current_app
# import requests, os, boto3 # could remove this (maybe others?) if i move pdf to its own file?
# from turtleapi import app
# import base64
# import io
# from sqlalchemy import *

model_mapping = {
    "LagoonEncounter": LagoonEncounter,
    "TridentEncounter": TridentEncounter,
    "BeachEncounter": BeachEncounter,
    "OffshoreEncounter": OffshoreEncounter,
    "LagoonMetadata": LagoonMetadata,
    "TridentMetadata": TridentMetadata,
    "OffshoreMetadata": OffshoreMetadata,
    "Clutch": Clutch,
    "Turtle": Turtle,
    "Net": Net,
    "IncidentalCapture": IncidentalCapture,
    "Tag": Tag,
    "Morphometrics": Morphometrics,
    "Sample": Sample,
    "SampleTracking": SampleTracking
}


def field_lister():
    data = {}

    for model in model_mapping:
        model_data = {}
        columns = model_mapping[model].__table__.c
        
        for c in columns:
            model_data[c.key] = c.type.python_type.__name__

        data[model] = model_data

    return data

def parse_query_filter(fieldname, filter, column):
    field_type = column.type.python_type
    # print(field_type)

    queries = []

    # Filter is blank; no filter / return all values for this column
    if filter is "":
        return queries
    
    # Case: string
    if field_type is str:
        print("it's a str")
        queries.append(column.contains(filter))

    # Case: int, float, date, time, etc.
    else:
        try:
            if "_" in filter:
                range = filter.split("_")
                queries.append(column >= range[0])
                queries.append(column <= range[1])
            else:
                queries.append(column == filter)
        except:
            print("ERROR HANDLING INPUT " + fieldname + " WITH GENERIC FILTER")
    
    return queries

def csv_export(data):
    string_io = StringIO()
    writer = csv.writer(string_io)

    buildup = {}

    ### Iterate over JSON and query for data
    for d in data:
        # Ignore invalid input (tables)
        if d not in model_mapping:
            print("Extra key (table), ignoring")
        else:
            table_columns = model_mapping[d].__table__.c
            fields = data[d]
            query_columns = []    # List of DB columns to query
            query_filters = []    # List of filters to apply to query

            for f in fields:
                # Check if field exists in database
                if f in table_columns:
                    query_columns.append(getattr(model_mapping[d], f))
                    query_filters.extend(parse_query_filter(f, fields[f], getattr(model_mapping[d], f)))
                else:
                    print("Extra key (field), ignoring")

            # Skip (very unlikely) empty query, where query_columns is None
            if query_columns:
                table_result = db.session.query(*query_columns).filter(*query_filters).all()       
                buildup[d] = table_result

    ### Create CSV
    # Write the header row
    header_row = []
    for b in buildup:
        for key in buildup[b][0].keys():
            header_row.append(b + "." + key)
    
    writer.writerow(header_row)
    
    # Write the body
    preceding_commas = []
    for b in buildup:
        for val in buildup[b]:
            writer.writerow(preceding_commas + list(val))
        for num_keys in buildup[b][0].keys():
            preceding_commas.append('')

    # Send the csv back to the user
    output = make_response(string_io.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output
    return {}