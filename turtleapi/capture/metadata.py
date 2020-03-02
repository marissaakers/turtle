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
    
    if data['environment_time'] is not None and data['environment_time'] != '':
        try:
            data['environment_time'] = datetime.strptime(data['environment_time'], '%H:%M:%S')
        except:
            print("Error: environment_time not in correct format")
            return {'error': 'environment_time not in correct format'}

    var_list = ('net_deploy_start_time','net_deploy_end_time','net_retrieval_start_time','net_retrieval_end_time')

    for x in data['nets']:
        for y in var_list:
            if x[y] is not None and x[y] != '':
                try:
                    x[y] = datetime.strptime(x[y], '%H:%M:%S')
                except:
                    print("Error: in nets,",y,"not in correct format")
                    return {'error': 'incorrect time format'}

    for x in data['incidental_captures']:
        if x['capture_time'] is not None and x['capture_time'] != '':
            try:
                x['capture_time'] = datetime.strptime(x['capture_time'], '%H:%M:%S')
            except:
                print("Error: in incidental captures, capture_time not in correct format")
                return {'error': 'incorrect time format'}

    metadata = LagoonMetadata.new_from_dict(data, error_on_extra_keys=False, drop_extra_keys=True)
    db.session.add(metadata)
    db.session.commit()

    return {'message': 'no errors'}

def query_trident_metadata(data):
    ### FILTERS
    FILTER_metadata_id = data.get('metadata_id', '')
    FILTER_metadata_date = data.get('metadata_date', '')
    FILTER_metadata_type = "trident"
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
        queries.append(TridentMetadata.metadata_id == FILTER_metadata_id)
    if (FILTER_metadata_date != ''):
        queries.append(TridentMetadata.metadata_date == FILTER_metadata_date)
    if (FILTER_metadata_id == FILTER_metadata_date):
        print("Error: Metadata query missing sufficient data")
        return {'error': 'Metadata query missing sufficient data'}

    # Grab metadata
    result = db.session.query(TridentMetadata).filter(*queries).first()
    if result is None:
        print("Error: Metadata matching criteria not found")
        return {'error': 'Metadata matching criteria not found'}

    result_encounter = result.to_dict(max_nesting=2)
    
    return Response(json.dumps(result_encounter, default = date_handler),mimetype = 'application/json')

def insert_trident_metadata(data):
    if data['metadata_date'] is not None and data['metadata_date'] != '':
        try:
            data['metadata_date'] = datetime.strptime(data['metadata_date'], '%m/%d/%Y')
        except:
            print("Error: metadata_date not in correct format")
            return {'error': 'metadata_date not in correct format'}
    
    if data['environment_time'] is not None and data['environment_time'] != '':
        try:
            data['environment_time'] = datetime.strptime(data['environment_time'], '%H:%M:%S')
        except:
            print("Error: environment_time not in correct format")
            return {'error': 'environment_time not in correct format'}

    var_list = ('net_deploy_start_time','net_deploy_end_time','net_retrieval_start_time','net_retrieval_end_time')

    for x in data['nets']:
        for y in var_list:
            if x[y] is not None and x[y] != '':
                try:
                    x[y] = datetime.strptime(x[y], '%H:%M:%S')
                except:
                    print("Error: in nets,",y,"not in correct format")
                    return {'error': 'incorrect time format'}

    for x in data['incidental_captures']:
        if x['capture_time'] is not None and x['capture_time'] != '':
            try:
                x['capture_time'] = datetime.strptime(x['capture_time'], '%H:%M:%S')
            except:
                print("Error: in incidental captures, capture_time not in correct format")
                return {'error': 'incorrect time format'}

    metadata = TridentMetadata.new_from_dict(data, error_on_extra_keys=False, drop_extra_keys=True)
    db.session.add(metadata)
    db.session.commit()

    return {'message': 'no errors'}

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

    var_list = ('capture_time', 'release_time')

    for x in var_list:
        if data[x] is not None and data[x] != '':
            try:
                data[x] = datetime.strptime(data[x], '%H:%M:%S')
            except:
                print("Error:",x,"not in correct format")
                return {'error': 'incorrect time format'}

    metadata = OffshoreMetadata.new_from_dict(data, error_on_extra_keys=False, drop_extra_keys=True)
    db.session.add(metadata)
    db.session.commit()

    return {'message': 'no errors'}
