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
    print("FILTER FUNCTION")
    print(fieldname)
    print(filter)
    print(column)

    field_type = column.type.python_type
    print(field_type)

    queries = []

    if filter is "":    # For any type, this implies no filter AKA return all
        return queries

    # Case: integer
    if field_type is int:
        print("it's an int")
        # int range
        if "_" in filter:
            range = filter.split("_")
            queries.append(column >= range[0])
            queries.append(column <= range[1])
        # one int
        else:
            queries.append(column == filter)

    # Case: date
    elif field_type is datetime.date:
        print("it's a date")
        if "_" in filter:
            range = filter.split("_")
            queries.append(column >= range[0])
            queries.append(column <= range[1])
        else:
            queries.append(column == filter)
    
    # Case: string
    elif field_type is str:
        print("it's a str")
        queries.append(column.contains(filter))

    else:
        print("currently unhandled")
    
    return queries

def csv_export(data):
    string_io = StringIO()
    writer = csv.writer(string_io)

    buildup = {}
    final_json = []
    queries = []

    for d in data: # Iterate over JSON
        if d not in model_mapping:  # Ignore invalid input (tables)
            print("Extra key (table), ignoring")
        else:
            table_columns = model_mapping[d].__table__.c
            fields = data[d]
            query_columns = []    # List of DB columns to query
            query_filters = []    # List of filters to apply to query

            for f in fields:
                if f in table_columns: # Check if field exists in database
                    query_columns.append(getattr(model_mapping[d], f))
                    query_filters.extend(parse_query_filter(f, fields[f], getattr(model_mapping[d], f)))
                else:
                    print("Extra key (field), ignoring")

            if query_columns:   # Handle (very unlikely) empty query
                table_result = db.session.query(*query_columns).filter(*query_filters).all()            
                buildup[d] = table_result


    #print(buildup['LagoonEncounter'])
    row_data = []
    for b in buildup:
        row_data.append(buildup[b])
    writer.writerow(row_data)

    # Send the csv back to the user
    output = make_response(string_io.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output
    return {}

    # for b in buildup:
    #     print(str(b) + str(buildup[b]))

        #result = db.session.query(LagoonEncounter, Turtle.turtle_id).filter().all()
        #print(result)
            
        # result = db.session.query(model_mapping[d]).all()
        # return result.to_dict()

    # # Write header row
    # writer.writerow([x for x in header_row])

    # # Get the total number of encounters (and thus rows)
    # rows_count = 0
    # for x in query_data:
    #     for y in x['encounters']:
    #         rows_count += 1

    # # Write data rows
    # for row in range(0, rows_count):
    #     row_data = []
    #     for x in header_row:
    #         if x in data:
    #             row_data.append(data[x][row])
    #     writer.writerow(row_data)

    # # Send the csv back to the user
    # output = make_response(string_io.getvalue())
    # output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    # output.headers["Content-type"] = "text/csv"
    # return output

    #return {}

            # print(result)
            # test = data[d]
            # for t in test:
            #     print(t)


    # print(model_list)

    # for model in model_list:
    #     if model is LagoonEncounter:
    #         table = model.__table__
    #         for column in table.c:
    #             print(column)




    # #test = LagoonEncounter.__table__.c + TridentEncounter.__table__.c # works
    # test = LagoonEncounter.__table__.c # includes table name
    # #test = [column.key for column in LagoonEncounter.__table__.columns] # just a str
    # #test = LagoonEncounter.__table__.columns.keys() # same as above, but better




    # print(test)
    # print("TEST!!!")
    # print(LagoonEncounter.__table__.name)
    # for item in test:
    #     print(item)
    #     # #print(str(item) + ' db: ' + str(item.type) + ' py: ' + str(item.type.python_type))
    #     # if item.type.python_type == int:
    #     #     #print("True")
    #     #     print(item)
    #     #     queries.append(item == 5)
    #     # else:
    #     #     #print("False")
    #     #     lol = False




    #result = db.session.query(LagoonEncounter).filter(queries).all()
    #result = db.session.query(lagoon_encounter).all()

    #print(test['encounter_id'])
    #print(type(LagoonEncounter.))

    # writer = csv.writer(string_io)

    # header_row = []
    # data = {}
    # if 'morphometrics' in features:
    #     morphometrics_data = [x['morphometrics'] for y in query_data for x in y['encounters']]
    #     morph_features = features['morphometrics']

    #     if 'curved_length' in morph_features or 'all' in morph_features:
    #         header_row.append('curved_length')
    #         data['curved_length'] = [x['curved_length'] for x in morphometrics_data]

    #     if 'straight_length' in morph_features or 'all' in morph_features:
    #         header_row.append('straight_length')
    #         data['straight_length'] = [x['straight_length'] for x in morphometrics_data]

    #     if 'minimum_length' in morph_features or 'all' in morph_features:
    #         header_row.append('minimum_length')
    #         data['minimum_length'] = [x['minimum_length'] for x in morphometrics_data]

    #     if 'plastron_length' in morph_features or 'all' in morph_features:
    #         header_row.append('plastron_length')
    #         data['plastron_length'] = [x['plastron_length'] for x in morphometrics_data]

    #     if 'weight' in morph_features or 'all' in morph_features:
    #         header_row.append('weight')
    #         data['weight'] = [x['weight'] for x in morphometrics_data]

    #     if 'curved_width' in morph_features or 'all' in morph_features:
    #         header_row.append('curved_width')
    #         data['curved_width'] = [x['curved_width'] for x in morphometrics_data]

    #     if 'straight_width' in morph_features or 'all' in morph_features:
    #         header_row.append('straight_width')
    #         data['straight_width'] = [x['straight_width'] for x in morphometrics_data]

    #     if 'tail_length_pl_vent' in morph_features or 'all' in morph_features:
    #         header_row.append('tail_length_pl_vent')
    #         data['tail_length_pl_vent'] = [x['tail_length_pl_vent'] for x in morphometrics_data]

    #     if 'tail_length_pl_tip' in morph_features or 'all' in morph_features:
    #         header_row.append('tail_length_pl_tip')
    #         data['tail_length_pl_tip'] = [x['tail_length_pl_tip'] for x in morphometrics_data]

    #     if 'head_width' in morph_features or 'all' in morph_features:
    #         header_row.append('head_width')
    #         data['head_width'] = [x['head_width'] for x in morphometrics_data]

    #     if 'body_depth' in morph_features or 'all' in morph_features:
    #         header_row.append('body_depth')
    #         data['body_depth'] = [x['body_depth'] for x in morphometrics_data]

    # if ('metadata' in features):
    #     metadata_data = [x['metadata'] for y in query_data for x in y['encounters']]

    #     if ('environment' in features['metadata']):
    #         env_features = features['metadata']['environment']
    #         environment_data = [x['environment'] for x in metadata_data]

    #         if 'water_sample' in env_features or 'all' in env_features:
    #             header_row.append('water_sample')
    #             data['water_sample'] = [x['water_sample'] for x in environment_data]

    #         if 'wind_speed' in env_features or 'all' in env_features:
    #             header_row.append('wind_speed')
    #             data['wind_speed'] = [x['wind_speed'] for x in environment_data]

    #         if 'wind_dir' in env_features or 'all' in env_features:
    #             header_row.append('wind_dir')
    #             data['wind_dir'] = [x['wind_dir'] for x in environment_data]

    #         if 'air_temp' in env_features or 'all' in env_features:
    #             header_row.append('air_temp')
    #             data['air_temp'] = [x['air_temp'] for x in environment_data]
            
    #         if 'water_temp_surface' in env_features or 'all' in env_features:
    #             header_row.append('water_temp_surface')
    #             data['water_temp_surface'] = [x['water_temp_surface'] for x in environment_data]

    #         if 'water_temp_1_m' in env_features or 'all' in env_features:
    #             header_row.append('water_temp_1_m')
    #             data['water_temp_1_m'] = [x['water_temp_1_m'] for x in environment_data]

    #         if 'water_temp_2_m' in env_features or 'all' in env_features:
    #             header_row.append('water_temp_2_m')
    #             data['water_temp_2_m'] = [x['water_temp_2_m'] for x in environment_data]

    #         if 'water_temp_6_m' in env_features or 'all' in env_features:
    #             header_row.append('water_temp_6_m')
    #             data['water_temp_6_m'] = [x['water_temp_6_m'] for x in environment_data]

    #         if 'water_temp_bottom' in env_features or 'all' in env_features:
    #             header_row.append('water_temp_bottom')
    #             data['water_temp_bottom'] = [x['water_temp_bottom'] for x in environment_data]

    #         if 'salinity_surface' in env_features or 'all' in env_features:
    #             header_row.append('salinity_surface')
    #             data['salinity_surface'] = [x['salinity_surface'] for x in environment_data]

    #         if 'salinity_1_m' in env_features or 'all' in env_features:
    #             header_row.append('salinity_1_m')
    #             data['salinity_1_m'] = [x['salinity_1_m'] for x in environment_data]

    #         if 'salinity_2_m' in env_features or 'all' in env_features:
    #             header_row.append('salinity_2_m')
    #             data['salinity_2_m'] = [x['salinity_2_m'] for x in environment_data]

    #         if 'salinity_6_m' in env_features or 'all' in env_features:
    #             header_row.append('salinity_6_m')
    #             data['salinity_6_m'] = [x['salinity_6_m'] for x in environment_data]

    #         if 'salinity_bottom' in env_features or 'all' in env_features:
    #             header_row.append('salinity_bottom')
    #             data['salinity_bottom'] = [x['salinity_bottom'] for x in environment_data]


    # # Write header row
    # writer.writerow([x for x in header_row])

    # # Get the total number of encounters (and thus rows)
    # rows_count = 0
    # for x in query_data:
    #     for y in x['encounters']:
    #         rows_count += 1

    # # Write data rows
    # for row in range(0, rows_count):
    #     row_data = []
    #     for x in header_row:
    #         if x in data:
    #             row_data.append(data[x][row])
    #     writer.writerow(row_data)

    # # Send the csv back to the user
    # output = make_response(string_io.getvalue())
    # output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    # output.headers["Content-type"] = "text/csv"
    # return output