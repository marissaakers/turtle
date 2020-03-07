from turtleapi import db
from turtleapi.models.turtlemodels import (LagoonEncounter, Encounter, Turtle, Tag,
                                           Morphometrics, Sample, Metadata, Net,
                                           IncidentalCapture)
from datetime import datetime, timedelta
import json
from turtleapi.capture.util import find_turtle_from_tags, date_handler
from flask import jsonify, Response

def insert_lagoon(data):

    data2 = {}
    data2['encounters'] = data
    data2['tags'] = data2['encounters']['tags']
    del data2['encounters']['tags']
    data2['species'] = data2['encounters']['species']
    del data2['encounters']['species']
    data2['encounters']['morphometrics'] = [data2['encounters']['morphometrics']]

    # handling turtle
    turtle = find_turtle_from_tags(data2['tags'])
    if turtle is not None:
        if data2['encounters']['capture_type'] != "strange recap": # need to make some check for this
            data2['encounters']['capture_type'] = "recap"
        metadata_id = data2['encounters']['metadata_id']
        encounter = LagoonEncounter.new_from_dict(data2['encounters'], error_on_extra_keys=False, drop_extra_keys=True)
        encounter.metadata_id = metadata_id
        del data2['encounters']

        compare_tags = db.session.query(Tag).filter(Tag.turtle_id==turtle.turtle_id,Tag.active==True)
        # updating existing tags
        for c in compare_tags:
            flag = False
            i = 0
            for i in range(len(data2['tags'])):
                if c.tag_number == data2['tags'][i]['tag_number']:
                    setattr(c,'tag_scars',data2['tags'][i]['tag_scars'])
                    flag = True
                    del data2['tags'][i]
                    break
                i = i + 1
            if flag == False:
                setattr(c,'active',False)
        # adding new tags
        for t in data2['tags']:
            tag = Tag.new_from_dict(t, error_on_extra_keys=False, drop_extra_keys=True)
            tag.turtle_id = turtle.turtle_id
            db.session.add(tag)
    else:
        if data2['encounters']['capture_type'] != "strange recap": # need to make some check for this
            data2['encounters']['capture_type'] = "new"
        metadata_id = data2['encounters']['metadata_id']
        encounter = LagoonEncounter.new_from_dict(data2['encounters'], error_on_extra_keys=False, drop_extra_keys=True)
        encounter.metadata_id = metadata_id
        del data2['encounters']
        turtle = Turtle.new_from_dict(data2, error_on_extra_keys=False, drop_extra_keys=True)

    encounter.turtle = turtle
    db.session.add(encounter)
    db.session.commit()

    return {'message': 'no errors'}

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

    FILTER_entered_by = data.get('entered_by')
    FILTER_verified_by = data.get('verified_by')
    FILTER_investigated_by = data.get('investigated_by')

    FILTER_metadata_id = data.get('metadata_id')
    FILTER_metadata_date = data.get('metadata_date')
    if FILTER_metadata_date is not None and FILTER_metadata_id is None: # Overwrite metadata_id only if it doesn't exist and we have a metadata_date asked
        FILTER_metadata_id = db.session.query(LagoonMetadata.metadata_id).filter(LagoonMetadata.metadata_date == FILTER_metadata_date).first()[0]
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

    result = db.session.query(LagoonEncounter.encounter_id, LagoonEncounter.encounter_date,Turtle.turtle_id, Turtle.species).filter(*queries, Turtle.turtle_id==Encounter.turtle_id).all() # returns list of result objects
    final_result = [x._asdict() for x in result] # json.dumps() strips the name of the field... convert to dict and json.dumps() saves it

    return Response(json.dumps(final_result, default = date_handler),mimetype = 'application/json')

def edit_lagoon(data):
    encounter_id = data.get('encounter_id')

    if encounter_id is None:
        return {'error': 'LagoonEncounter edit input is in invalid format'}
    
    edit_encounter = db.session.query(LagoonEncounter).filter(LagoonEncounter.encounter_id == encounter_id).first()

    if edit_encounter is not None:
        new_encounter_values = edit_encounter.to_dict()         # Get current DB values
        new_encounter_values.update(data)                       # Update with any new values from incoming JSON
        edit_encounter.update_from_dict(new_encounter_values)   # Update DB entry
        
        db.session.commit()                                     # commit changes to DB

        return {'message':'Lagoon encounter edited successfully'}

    return {'message':'No matching lagoon encounters found'}