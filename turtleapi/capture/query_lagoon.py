from turtleapi import db
from turtleapi.models.turtlemodels import (LagoonEncounter, Encounter, Turtle, 
Tag, Morphometrics, Sample, Metadata, Net, IncidentalCapture)
from datetime import datetime, timedelta
import json
from flask import jsonify
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
    result = db.session.query(Encounter,Turtle).filter(*queries, Turtle.turtle_id==Encounter.turtle_id).first()
    print(result)
    result_encounter = result[0]
    result_turtle = result[1]

    # Make output object
    # output = result.to_dict(max_nesting=1)
    output = result_turtle.to_dict(max_nesting=2)
    #print(output)
    # output = result.dump_to_dict(max_nesting=4)

    # Grab tags
    # turtle_id = output['turtle_id']
    # tag_result = Tag.query.filter_by(turtle_id=turtle_id).all()
    # output['tags'] = tag_schema.dump(tag_result, many=True)
    
    #resp = Response(response=output, status=200, mimetype="application/json")
    #return(resp)
    return jsonify(output)

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

    queries.append(Encounter.type == "lagoon")

    result = db.session.query(Encounter,Turtle).filter(*queries, Turtle.turtle_id==Encounter.turtle_id).all()
    encounters = [x[0] for x in result]
    turtles = [x[1] for x in result]

    output = [x.to_dict() for x in encounters]
    output2 = [x.to_dict() for x in turtles]

    loop_length = len(output)
    for x in range(0,loop_length):
        output[x].update(output2[x])

    # output = [x.to_dict() for x in result]

    final_encounter = [x.to_json(serialize_function=my_custom_serializer,  filter_fields = ['turtle_id', 'encounter_id']) for x in encounters]

    return jsonify(final_encounter)