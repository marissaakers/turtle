from turtleapi import db
from turtleapi.models.turtlemodels import (LagoonEncounter, Encounter, Turtle, 
Tag, Morphometrics, Sample, Metadata, Net, IncidentalCapture, LagoonMetadata)
from turtleapi.capture.util import date_handler
from datetime import datetime, timedelta
import json
from flask import jsonify, Response
from turtleapi.capture.util import find_turtles_from_tags, my_custom_serializer

def query_lagoon(data):

    # Filters
    FILTER_encounter_id = data.get('encounter_id')

    # Error out if no encounter_id
    if FILTER_encounter_id is None:
        print("error: no encounter id provided to full lagoon query")
        return {'error': 'no encounter id provided to full lagoon query'}
    
    # Build queries
    queries = []

    queries.append(Encounter.encounter_id == FILTER_encounter_id)
    queries.append(Encounter.type == "lagoon")

    # Grab turtles
    result = db.session.query(Encounter, Turtle.species).filter(*queries, Turtle.turtle_id==Encounter.turtle_id).first()

    if result is None:
        return {'error': 'No encounter with that ID exists'}

    # Add species
    result_encounter = result[0].to_dict(max_nesting=2)
    result_encounter['species'] = result[1]
    
    # Grab tags
    tags = db.session.query(Tag).filter(Tag.turtle_id==result_encounter['turtle_id']).all()
    result_encounter['tags'] = [x.to_dict() for x in tags]

    return Response(json.dumps(result_encounter, default = date_handler),mimetype = 'application/json')

def mini_query_lagoon(data):

    ### Filters
    FILTER_tags = data.get('tags')
    FILTER_species = data.get('species') # Only match this species

    FILTER_encounter_date_start = data.get('encounter_date_start') # Match between FILTER_DATE_START and FILTER_DATE_END
    FILTER_encounter_date_end = data.get('encounter_date_end')

    # Try to parse dates
    if FILTER_encounter_date_start is not None:
        try:
            FILTER_encounter_date_start = datetime.strptime(FILTER_encounter_date_start, '%m/%d/%Y') # .date()
        except: 
            print("Error: date not in correct format")
            FILTER_encounter_date_start = None
    if FILTER_encounter_date_end is not None:
        try:
            FILTER_encounter_date_end = datetime.strptime(FILTER_encounter_date_end, '%m/%d/%Y')
        except: 
            print("Error: date not in correct format")
            FILTER_encounter_date_end = None

    FILTER_entered_by = data.get('entered_by')
    FILTER_verified_by = data.get('verified_by')
    FILTER_investigated_by = data.get('investigated_by')

    FILTER_metadata_id = data.get('metadata_id')
    FILTER_metadata_date = data.get('metadata_date')
    if FILTER_metadata_date is not None and FILTER_metadata_id is None: # Overwrite metadata_id only if it doesn't exist and we have a metadata_date asked
        try:
            FILTER_metadata_date = datetime.strptime(FILTER_metadata_date, '%m/%d/%Y')
            FILTER_metadata_id = db.session.query(LagoonMetadata.metadata_id).filter(LagoonMetadata.metadata_date == FILTER_metadata_date).first()[0]
        except: 
            print("Error: date not in correct format")
            FILTER_metadata_date = None
        
        if FILTER_metadata_id is None:  # If date doesn't match anything, make sure we return no results
            FILTER_metadata_id = -1
    
    # If tags, find IDs and search by ID
    FILTER_turtle_ids = None
    if FILTER_tags is not None:
        FILTER_turtle_ids = find_turtles_from_tags(FILTER_tags)

    ### End filters

    queries = []

    if FILTER_turtle_ids is not None:
        queries.append(Encounter.turtle_id.in_(FILTER_turtle_ids))
    if FILTER_encounter_date_start is not None:
        queries.append(Encounter.encounter_date >= FILTER_encounter_date_start)
    if FILTER_encounter_date_end is not None:
        queries.append(Encounter.encounter_date <= FILTER_encounter_date_end)
    if FILTER_entered_by is not None:
        queries.append(Encounter.entered_by == FILTER_entered_by)
    if FILTER_verified_by is not None:
        queries.append(Encounter.entered_by == FILTER_verified_by)
    if FILTER_investigated_by is not None:
        queries.append(Encounter.entered_by == FILTER_investigated_by)
    if FILTER_species is not None:
        queries.append(Turtle.species == FILTER_species)
    if FILTER_metadata_id is not None:
        queries.append(Encounter.metadata_id == FILTER_metadata_id)

    queries.append(Encounter.type == "lagoon")

    result = db.session.query(LagoonEncounter.encounter_id, LagoonEncounter.encounter_date,Turtle.turtle_id, Turtle.species).filter(*queries, Turtle.turtle_id==Encounter.turtle_id).all()

    # final_result = [x.to_json(serialize_function=my_custom_serializer,  filter_fields = ['turtle_id', 'encounter_id']) for x in encounters]

    return jsonify(result)
