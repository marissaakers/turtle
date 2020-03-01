from turtleapi import db
from turtleapi.models.turtlemodels import (LagoonEncounter, Encounter, Turtle, 
Tag, Morphometrics, Sample, Metadata, Net, IncidentalCapture, LagoonMetadata,
TridentMetadata, OffshoreMetadata)
from datetime import datetime, timedelta
import json
from flask import jsonify
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

    queries.append(Metadata.type == "lagoon")
    if (FILTER_metadata_id != ''):
        queries.append(Metadata.metadata_id == FILTER_metadata_id)
    if (FILTER_metadata_date != ''):
        queries.append(Metadata.metadata_date == FILTER_metadata_date)
    if (FILTER_metadata_id == FILTER_metadata_date):
        print("Error: Metadata query missing sufficient data")
        return {'error': 'Metadata query missing sufficient data'}

    # Grab metadata
    result = db.session.query(Metadata).filter(*queries).first()
    result_encounter = result.to_dict(max_nesting=1)

    # Grab nets
    nets = db.session.query(Net).filter(Net.metadata_id==result_encounter['metadata_id']).all()
    result_encounter['nets'] = [x.to_dict() for x in nets]

    # Grab incidental captures
    incidental_captures = db.session.query(IncidentalCapture).filter(IncidentalCapture.metadata_id==result_encounter['metadata_id']).all()
    result_encounter['incidental_captures'] = [x.to_dict() for x in incidental_captures]

    return jsonify(result_encounter)

def insert_lagoon_metadata(data):
    # Declare schema instances
    metadata_schema = MetadataSchema()
    net_schema = NetSchema()
    incidental_capture_schema = IncidentalCaptureSchema()

    nets = data['nets']
    incidental_captures = data['incidental_captures']

    net_list = ()
    for net in nets:
        new_net = Net(
            metadata=metadata_item,
            net_number=net['net_number'],
            net_deploy_start_time=net['net_deploy_start_time'],
            net_deploy_end_time=net['net_deploy_end_time'],
            net_retrieval_start_time=net['net_retrieval_start_time'],
            net_retrieval_end_time=net['net_retrieval_end_time']
        )
        net_list = net_list + (new_net,)

    metadata_item = Metadata(
        metadata_date=data['metadata_date'],
        metadata_location=data['metadata_location'],
        metadata_investigators=data['metadata_investigators'],
        number_of_cc_captured=data['number_of_cc_captured'],
        number_of_cm_captured=data['number_of_cm_captured'],
        number_of_other_captured=data['number_of_other_captured'],
        water_sample=data['water_sample'],
        wind_speed=data['wind_speed'],
        wind_dir=data['wind_dir'],
        environment_time=data['environment_time'],
        weather=data['weather'],
        air_temp=data['air_temp'],
        water_temp_surface=data['water_temp_surface'],
        water_temp_1_m=data['water_temp_1_m'],
        water_temp_2_m=data['water_temp_2_m'],
        water_temp_6_m=data['water_temp_6_m'],
        water_temp_bottom=data['water_temp_bottom'],
        salinity_surface=data['salinity_surface'],
        salinity_1_m=data['salinity_1_m'],
        salinity_2_m=data['salinity_2_m'],
        salinity_6_m=data['salinity_6_m'],
        salinity_bottom=data['salinity_bottom']
    )

    incidental_capture_list = ()
    for incidental_capture in incidental_captures:
        new_incidental_capture = IncidentalCapture(
            metadata=metadata_item,
            species=incidental_capture['species'],
            capture_time=incidental_capture['capture_time'],
            measurement=incidental_capture['measurement'],
            notes=incidental_capture['notes']
        )
        incidental_capture_list = incidental_capture_list + (new_incidental_capture,)

    db.session.add(metadata_item)
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

    queries.append(Metadata.type == "trident")
    if (FILTER_metadata_id != ''):
        queries.append(Metadata.metadata_id == FILTER_metadata_id)
    if (FILTER_metadata_date != ''):
        queries.append(Metadata.metadata_date == FILTER_metadata_date)
    if (FILTER_metadata_id == FILTER_metadata_date):
        print("Error: Metadata query missing sufficient data")
        return {'error': 'Metadata query missing sufficient data'}

    # Grab metadata
    result = db.session.query(Metadata).filter(*queries).first()
    result_encounter = result.to_dict(max_nesting=1)

    # Grab nets
    nets = db.session.query(Net).filter(Net.metadata_id==result_encounter['metadata_id']).all()
    result_encounter['nets'] = [x.to_dict() for x in nets]

    # Grab incidental captures
    incidental_captures = db.session.query(IncidentalCapture).filter(IncidentalCapture.metadata_id==result_encounter['metadata_id']).all()
    result_encounter['incidental_captures'] = [x.to_dict() for x in incidental_captures]

    return jsonify(result_encounter)

def insert_trident_metadata(data):
    return {'message': 'no errors'}

def query_offshore_metadata(data):
    ### FILTERS
    FILTER_metadata_id = data.get('metadata_id', '')
    FILTER_capture_date = data.get('capture_date', '')
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

    queries.append(Metadata.type == "offshore")
    if (FILTER_metadata_id != ''):
        queries.append(Metadata.metadata_id == FILTER_metadata_id)
    if (FILTER_capture_date != ''):
        queries.append(Metadata.metadata_date == FILTER_capture_date)
    if (FILTER_metadata_id == FILTER_capture_date):
        print("Error: Metadata query missing sufficient data")
        return {'error': 'Metadata query missing sufficient data'}

    # Grab metadata
    result = db.session.query(Metadata).filter(*queries).first()
    result_encounter = result.to_dict(max_nesting=1)

    # Grab nets
    nets = db.session.query(Net).filter(Net.metadata_id==result_encounter['metadata_id']).all()
    result_encounter['nets'] = [x.to_dict() for x in nets]

    # Grab incidental captures
    incidental_captures = db.session.query(IncidentalCapture).filter(IncidentalCapture.metadata_id==result_encounter['metadata_id']).all()
    result_encounter['incidental_captures'] = [x.to_dict() for x in incidental_captures]

    return jsonify(result_encounter)

def insert_offshore_metadata(data):
    return {'message': 'no errors'}
