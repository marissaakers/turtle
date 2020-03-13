from turtleapi import db
from turtleapi.models.turtlemodels import (BeachEncounter, Encounter, Turtle, Tag,
                                           Morphometrics, Sample, Clutch)
from datetime import datetime, timedelta
import json
from turtleapi.capture.util import find_turtle_from_tags, date_handler, get_miniquery_filters, generate_miniquery_queries
from flask import jsonify, Response
import random # we can remove this when we're done and don't do the manual test insertions anymore

def mini_query_beach(data):
    filters = get_miniquery_filters(data)

    # no metadata, so no filtering by metadata, will just abide by filters already present

    queries = generate_miniquery_queries(filters, BeachEncounter)

    result = db.session.query(BeachEncounter.encounter_id, BeachEncounter.encounter_date, Turtle.turtle_id, Turtle.species).filter(*queries, Turtle.turtle_id==Encounter.turtle_id).all() # returns list of result objects
    final_result = [x._asdict() for x in result] # json.dumps() strips the name of the field... convert to dict and json.dumps() saves it

    return Response(json.dumps(final_result, default = date_handler),mimetype = 'application/json')

def query_beach(data):
    # Filters
    FILTER_encounter_id = data.get('encounter_id')

    # Error out if no encounter_id
    if FILTER_encounter_id is None:
        print("error: no encounter id provided to full beach query")
        return {'error': 'no encounter id provided to full beach query'}
    
    # Build queries
    queries = []

    queries.append(Encounter.encounter_id == FILTER_encounter_id)
    queries.append(Encounter.type == "beach")

    # Grab turtles
    result = db.session.query(Encounter, Turtle.species).filter(*queries, Turtle.turtle_id==Encounter.turtle_id).first()

    if result is None:
        return {'error': 'No encounter with that ID exists'}

    # Add species
    result_encounter = result[0].to_dict(max_nesting=5)
    result_encounter['species'] = result[1]
    
    # Grab tags
    tags = db.session.query(Tag).filter(Tag.turtle_id==result_encounter['turtle_id']).all()
    result_encounter['tags'] = [x.to_dict() for x in tags]

    # Grab clutches
    clutches = db.session.query(Clutch).filter(Clutch.turtle_id==result_encounter['turtle_id']).all()
    result_encounter['clutches'] = [x.to_dict() for x in clutches]

    return Response(json.dumps(result_encounter, default = date_handler),mimetype = 'application/json')

def insert_beach(data):
    data2 = {}
    data2['encounters'] = data
    data2['tags'] = data2['encounters']['tags']
    del data2['encounters']['tags']
    data2['clutches'] = [data2['encounters']['clutches']]
    del data2['encounters']['clutches']
    data2['species'] = data2['encounters']['species']
    del data2['encounters']['species']
    data2['encounters']['morphometrics'] = [data2['encounters']['morphometrics']]

    # handling turtle
    turtle = find_turtle_from_tags(data2['tags'])
    if turtle is not None:
        if data2['encounters']['capture_type'] != "strange recap": # need to make some check for this
            data2['encounters']['capture_type'] = "recap"
        encounter = BeachEncounter.new_from_dict(data2['encounters'], error_on_extra_keys=False, drop_extra_keys=True)
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
        clutch = Clutch.new_from_dict(data2['clutches'][0], error_on_extra_keys=False, drop_extra_keys=True)
        clutch.turtle_id = turtle.turtle_id
        db.session.add(clutch)
    else:
        if data2['encounters']['capture_type'] != "strange recap": # need to make some check for this
            data2['encounters']['capture_type'] = "new"
        encounter = BeachEncounter.new_from_dict(data2['encounters'], error_on_extra_keys=False, drop_extra_keys=True)
        del data2['encounters']
        turtle = Turtle.new_from_dict(data2, error_on_extra_keys=False, drop_extra_keys=True)

    encounter.turtle = turtle
    db.session.add(encounter)
    db.session.commit()

    return {'message': 'no errors'}

def edit_beach(data):
    return {'message': 'WIP'}

def delete_beach(data):
    encounter_id = data.get('encounter_id')

    if encounter_id is None:
        return {'error': 'BeachEncounter delete input is in invalid format'}
    
    edit_encounter = db.session.query(BeachEncounter).filter(BeachEncounter.encounter_id == encounter_id).first()

    if edit_encounter is not None:
        db.session.delete(edit_encounter)   # Get current DB values
        db.session.commit()                 # commit changes to DB

        return {'message':'Beach encounter deleted successfully'}

    return {'message':'No matching beach encounter found'}