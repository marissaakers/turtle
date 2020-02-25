from turtleapi import db
from turtleapi.models.turtlemodels import (LagoonEncounter, Encounter, Turtle, 
Tag, Morphometrics, Sample, Metadata, Net, IncidentalCapture,
TurtleSchema, EncounterSchema, TagSchema, MorphometricsSchema, MetadataSchema,
LagoonEncounterSchema, SampleSchema, NetSchema, IncidentalCaptureSchema, LagoonQuerySchema, FullLagoonQuerySchema)
from datetime import datetime, timedelta
import json
from flask import jsonify
from turtleapi.capture.util import find_turtles_from_tags

def query_lagoon(data):

    # Declare schema instances
    tag_schema = TagSchema()
    full_lagoon_query_schema = FullLagoonQuerySchema()

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
    result_encounter = result[0]

    # Make output object
    output = full_lagoon_query_schema.dump(result_encounter)

    # Grab tags
    turtle_id = output['turtle_id']
    tag_result = Tag.query.filter_by(turtle_id=turtle_id).all()
    output['tags'] = tag_schema.dump(tag_result, many=True)

    return output

def mini_query_lagoon(data):

    # Declare schema instances
    lagoon_query_schema = LagoonQuerySchema()

    ### Filters
    FILTER_tags = data.get('tags', '')
    FILTER_species = data.get('species', '') # Only match this species

    string_date_start = data.get('encounter_date_start', '') # Match between FILTER_DATE_START and FILTER_DATE_END
    string_date_end = data.get('encounter_date_end', '')
    if string_date_start != '':
        try:
            FILTER_encounter_date_start = datetime.strptime(string_date_start, '%m/%d/%Y') # .date()
        except: 
            print("Error: date not in correct format")
    if string_date_end != '':
        try:
            FILTER_encounter_date_end = datetime.strptime(string_date_end, '%m/%d/%Y')
        except: 
            print("Error: date not in correct format")

    FILTER_entered_by = data.get('entered_by', '')
    FILTER_turtle_ids = ''
    if FILTER_tags != '':
        FILTER_turtle_ids = find_turtles_from_tags(FILTER_tags)

    ### End filters

    queries = []

    if FILTER_turtle_ids != '':
        queries.append(Encounter.turtle_id.in_(FILTER_turtle_ids))
    if string_date_start != '':
        queries.append(Encounter.encounter_date >= FILTER_encounter_date_start)
    if string_date_end != '':
        queries.append(Encounter.encounter_date <= FILTER_encounter_date_end)
    if FILTER_entered_by != '':
        queries.append(Encounter.entered_by == FILTER_entered_by)
    if FILTER_species != '':
        queries.append(Turtle.species == FILTER_species)

    queries.append(Encounter.type == "lagoon")

    result = db.session.query(Encounter,Turtle).filter(*queries, Turtle.turtle_id==Encounter.turtle_id).all()
    encounters = [x[0] for x in result]

    output = lagoon_query_schema.dump(encounters, many=True)
    return output