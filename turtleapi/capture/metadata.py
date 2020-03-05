from turtleapi import db
from turtleapi.models.turtlemodels import (LagoonEncounter, Encounter, Turtle, 
Tag, Morphometrics, Sample, Metadata, Net, IncidentalCapture, LagoonMetadata,
TridentMetadata, OffshoreMetadata)
from turtleapi.capture.util import date_handler
from datetime import datetime, timedelta
import json
from flask import Response
from turtleapi.capture.util import find_turtles_from_tags

def query_lagoon_metadata(data):
    ### FILTERS
    FILTER_metadata_id = data.get('metadata_id', '')
    FILTER_metadata_date = data.get('metadata_date', '')
    FILTER_metadata_type = "lagoon"
    if FILTER_metadata_date != '':
        try:
            FILTER_metadata_date = datetime.strptime(FILTER_metadata_date, '%m/%d/%Y')
        except: 
            print("Error: date not in correct format")
            FILTER_metadata_date = ''
    ### END FILTERS

    # Build queries
    queries = []

    # queries.append(Metadata.type == "lagoon")
    if (FILTER_metadata_id != ''):
        queries.append(LagoonMetadata.metadata_id == FILTER_metadata_id)
    if (FILTER_metadata_date != ''):
        queries.append(LagoonMetadata.metadata_date == FILTER_metadata_date)
    if (FILTER_metadata_id == FILTER_metadata_date):
        print("Error: Metadata query missing sufficient data")
        return {'error': 'Metadata query missing sufficient data'}

    # Grab metadata
    result = db.session.query(LagoonMetadata).filter(*queries).first()
    if result is None:
        print("Error: Metadata matching criteria not found")
        return {'error': 'Metadata matching criteria not found'}

    result_encounter = result.to_dict(max_nesting=2)
    
    return Response(json.dumps(result_encounter, default = date_handler),mimetype = 'application/json')

def insert_lagoon_metadata(data):
    if data['metadata_date'] is not None and data['metadata_date'] != '':
        try:
            data['metadata_date'] = datetime.strptime(data['metadata_date'], '%m/%d/%Y')
        except:
            print("Error: metadata_date not in correct format")
            return {'error': 'metadata_date not in correct format'}

    metadata = LagoonMetadata.new_from_dict(data, error_on_extra_keys=False, drop_extra_keys=True)
    db.session.add(metadata)
    db.session.commit()

    return {'message': 'no errors'}

def edit_lagoon_metadata(data):
    metadata_id = data.get('metadata_id')

    if metadata_id is None:
        return {'error': 'LagoonMetadata edit input is in invalid format'}
    
    edit_metadata = db.session.query(LagoonMetadata).filter(LagoonMetadata.metadata_id == metadata_id).first()

    # if edit_metadata is not None:
    #     new_metadata_values = edit_metadata.to_dict()           # Get current DB values
    #     new_metadata_values.update(data)                        # Update with any new values from incoming JSON
    #     edit_metadata.update_from_dict(new_metadata_values)     # Update DB entry
        
    #     db.session.commit()                                     # commit changes to DB

    #     return {'message':'Lagoon metadata edited successfully'}

    # return {'message':'No matching lagoon metadatas found'}
    return edit_metadata.to_json()


def query_offshore_metadata(data):
    ### FILTERS
    FILTER_metadata_id = data.get('metadata_id', '')
    FILTER_capture_date= data.get('capture_date', '')
    FILTER_metadata_type = "offshore"
    if FILTER_capture_date != '':
        try:
            FILTER_capture_date = datetime.strptime(FILTER_capture_date, '%m/%d/%Y')
        except: 
            print("Error: date not in correct format")
            FILTER_capture_date = ''
    ### END FILTERS

    # Build queries
    queries = []

    # queries.append(Metadata.type == "lagoon")
    if (FILTER_metadata_id != ''):
        queries.append(OffshoreMetadata.metadata_id == FILTER_metadata_id)
    if (FILTER_capture_date != ''):
        queries.append(OffshoreMetadata.capture_date == FILTER_capture_date)
    if (FILTER_metadata_id == FILTER_capture_date):
        print("Error: Metadata query missing sufficient data")
        return {'error': 'Metadata query missing sufficient data'}

    # Grab metadata
    result = db.session.query(OffshoreMetadata).filter(*queries).first()
    if result is None:
        print("Error: Metadata matching criteria not found")
        return {'error': 'Metadata matching criteria not found'}

    result_encounter = result.to_dict(max_nesting=2)
    
    return Response(json.dumps(result_encounter, default = date_handler),mimetype = 'application/json')

def insert_offshore_metadata(data):
    if data['capture_date'] is not None and data['capture_date'] != '':
        try:
            data['capture_date'] = datetime.strptime(data['capture_date'], '%m/%d/%Y')
        except:
            print("Error: capture_date not in correct format")
            return {'error': 'capture_date not in correct format'}

    metadata = OffshoreMetadata.new_from_dict(data, error_on_extra_keys=False, drop_extra_keys=True)
    db.session.add(metadata)
    db.session.commit()

    return {'message': 'no errors'}
