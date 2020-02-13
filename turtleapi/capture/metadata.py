from turtleapi import db
from turtleapi.models.turtlemodels import (LagoonEncounter, Encounter, Turtle, 
Tag, Morphometrics, Sample, Metadata, Net, IncidentalCapture,
TurtleSchema, EncounterSchema, TagSchema, MorphometricsSchema, MetadataSchema,
LagoonEncounterSchema, SampleSchema, NetSchema, IncidentalCaptureSchema)
from datetime import datetime, timedelta
import json
from flask import jsonify
from turtleapi.capture.util import find_turtles_from_tags

def query_metadata(data):
    # Declare schema instances
    metadata_schema = MetadataSchema()
    net_schema = NetSchema()
    incidental_capture_schema = IncidentalCaptureSchema()
    # environment_schema = EnvironmentSchema()
    
    ### FILTERS
    FILTER_metadata_id = data.get('metadata_id', '')
    FILTER_metadata_date = data.get('metadata_date', '')
    ### END FILTERS

    metadata_result = None
    if FILTER_metadata_id != '':
        metadata_result = Metadata.query.filter_by(metadata_id=FILTER_metadata_id).first()
    elif FILTER_metadata_date != '':
        metadata_result = Metadata.query.filter_by(metadata_date=FILTER_metadata_date).first()

    if metadata_result is not None:
        output = metadata_schema.dump(metadata_result)
        metadata_id = output['metadata_id']
        
        # Grab nets
        nets_result = Net.query.filter_by(metadata_id=metadata_id).all()
        output['nets'] = net_schema.dump(nets_result, many=True)

        # Grab incidental captures
        incidental_captures_result = IncidentalCapture.query.filter_by(metadata_id=metadata_id).all()
        output['incidental_captures'] = incidental_capture_schema.dump(incidental_captures_result, many=True)

        # # Grab environment
        # environment_result = Environment.query.filter_by(metadata_id=metadata_id).first()
        # output['environment'] = environment_schema.dump(environment_result)
        
        return output
    else:
        print("error: Metadata input is in invalid format")
        return {'error': 'Metadata input is in invalid format'}

# Untested
def insert_metadata(data):
    # Declare schema instances
    metadata_schema = MetadataSchema()
    net_schema = NetSchema()
    incidental_capture_schema = IncidentalCaptureSchema()
    environment_schema = EnvironmentSchema()

    nets = data['nets']
    environment = data['environment']
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

    environment_item = Environment(
        metadata=metadata_item,
        water_sample=environment['water_sample'],
        wind_speed=environment['wind_speed'],
        wind_dir=environment['wind_dir'],
        environment_time=environment['environment_time'],
        weather=environment['weather'],
        air_temp=environment['air_temp'],
        water_temp_surface=environment['water_temp_surface'],
        water_temp_1_m=environment['water_temp_1_m'],
        water_temp_2_m=environment['water_temp_2_m'],
        water_temp_6_m=environment['water_temp_6_m'],
        water_temp_bottom=environment['water_temp_bottom'],
        salinity_surface=environment['salinity_surface'],
        salinity_1_m=environment['salinity_1_m'],
        salinity_2_m=environment['salinity_2_m'],
        salinity_6_m=environment['salinity_6_m'],
        salinity_bottom=environment['salinity_bottom']
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

    db.session.add(environment_item)
    db.session.commit()
    return None