from turtleapi import db
from turtleapi.models.turtlemodels import (BeachEncounter, Encounter, Turtle, Tag,
                                           Morphometrics, Sample, Clutch)
from datetime import datetime, timedelta
import json
from turtleapi.capture.util import find_turtle_from_tags, date_handler, get_miniquery_filters, generate_miniquery_queries
from flask import jsonify, Response
import random # we can remove this when we're done and don't do the manual test insertions anymore

# returns encounter_id, encounter_date, turtle_id, species, and stake_number assoc. w/beach encounter
def mini_query_beach(data):
    filters = get_miniquery_filters(data)

    # no metadata, so no filtering by metadata, will just abide by filters already present

    queries = generate_miniquery_queries(filters, BeachEncounter)

    result = db.session.query(BeachEncounter.encounter_id, BeachEncounter.encounter_date, Turtle.turtle_id, Turtle.species, Clutch.stake_number).filter(*queries, Turtle.turtle_id==Encounter.turtle_id, Clutch.encounter_id==Encounter.encounter_id).order_by(BeachEncounter.encounter_date.desc()).all() # returns list of result objects
    final_result = [x._asdict() for x in result] # json.dumps() strips the name of the field... convert to dict and json.dumps() saves it

    return Response(json.dumps(final_result, default = date_handler),mimetype = 'application/json')

# returns a complete beach encounter (w/clutch, morphometrics, turtle information, tags, samples)
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
    result = db.session.query(Encounter, Turtle.species, Turtle.sex).filter(*queries, Turtle.turtle_id==Encounter.turtle_id).first()

    if result is None:
        return {'error': 'No encounter with that ID exists'}

    # Add species
    result_encounter = result[0].to_dict(max_nesting=2)
    result_encounter['species'] = result[1]
    result_encounter['sex'] = result[2]
    
    # Grab tags
    if (result_encounter['tag1'] == result_encounter['tag2'] and result_encounter['tag1'] == result_encounter['tag3']):
        tags = db.session.query(Tag).filter(Tag.turtle_id==result_encounter['turtle_id']).all()
        result_encounter['tags'] = [x.to_dict() for x in tags]
    else:
        taglist = [result_encounter['tag1'], result_encounter['tag2'], result_encounter['tag3']]
        tags = db.session.query(Tag).filter(Tag.tag_number.in_(taglist)).all()
        result_encounter['tags'] = [x.to_dict() for x in tags]

    return Response(json.dumps(result_encounter, default = date_handler),mimetype = 'application/json')

# inserts all info assoc. w/beach encounter
def insert_beach(data):
    data2 = {}
    data2['encounters'] = data
    data2['tags'] = data2['encounters']['tags']
    del data2['encounters']['tags']
    data2['species'] = data2['encounters']['species']
    del data2['encounters']['species']
    data2['sex'] = data2['encounters']['sex']
    del data2['encounters']['sex']
    data2['encounters']['morphometrics'] = [data2['encounters']['morphometrics']]
    data2['encounters']['clutches'] = [data2['encounters']['clutches']]

    # handling tag references in encounter
    j = 0
    tagfield = ['tag1', 'tag2', 'tag3']
    for t in data2['tags']:
        data2['encounters'][tagfield[j]] = t['tag_number']
        j = j + 1

    # handling turtle
    turtle = find_turtle_from_tags(data2['tags'])
    # turtle is a recapture
    if turtle is not None:
        if data2['encounters']['capture_type'] != "strange recap":
            data2['encounters']['capture_type'] = "recap"

        compare_tags = db.session.query(Tag).filter(Tag.turtle_id==turtle.turtle_id,Tag.active==True)
        # updating existing tags
        for c in compare_tags:
            flag = False
            i = 0
            for i in range(len(data2['tags'])):
                if c.tag_number == data2['tags'][i]['tag_number']:
                    flag = True
                    del data2['tags'][i]
                    break
            if flag == False:
                setattr(c,'active',False)
        # adding new tags
        for t in data2['tags']:
            # handling strange tags
            if t['isNew'] == False:
                data2['encounters']['capture_type'] = "strange recap"
            tag = Tag.new_from_dict(t, error_on_extra_keys=False, drop_extra_keys=True)
            tag.turtle_id = turtle.turtle_id
            db.session.add(tag)
        
        encounter = BeachEncounter.new_from_dict(data2['encounters'], error_on_extra_keys=False, drop_extra_keys=True)
    # turtle is a new capture
    else:
        if data2['encounters']['capture_type'] != "strange recap":
            data2['encounters']['capture_type'] = "new"

        # handling strange tags
        for t in data2['tags']:
            if t['isNew'] == False:
                data2['encounters']['capture_type'] = "strange recap"
        
        encounter = BeachEncounter.new_from_dict(data2['encounters'], error_on_extra_keys=False, drop_extra_keys=True)
        del data2['encounters']

        turtle = Turtle.new_from_dict(data2, error_on_extra_keys=False, drop_extra_keys=True)

    encounter.turtle = turtle
    db.session.add(encounter)
    db.session.commit()

    return {'message': 'no errors', 'encounter_id': encounter.encounter_id}

# editing a beach encounter and all assoc. tables
def edit_beach(data):
    # editing turtle
    turtle = data.get('turtle')
    if turtle is not None:
        turtle_id = turtle.get('turtle_id')
        if turtle_id is not None:
            edit_turtle = db.session.query(Turtle).filter(Turtle.turtle_id == turtle_id).first()
            if edit_turtle is not None:
                new_turtle_values = edit_turtle.to_dict()       # Get current DB values
                new_turtle_values.update(turtle)                # Update with any new values from incoming JSON
                edit_turtle.update_from_dict(new_turtle_values) # Update DB entry

    # editing actual encounter instance
    encounter = data.get('encounter')
    if encounter is not None:
        encounter_id = encounter.get('encounter_id')
        if encounter_id is not None:
            edit_encounter = db.session.query(BeachEncounter).filter(BeachEncounter.encounter_id == encounter_id).first()
            # return Response(json.dumps(edit_encounter.to_dict(max_nesting=5), default = date_handler),mimetype = 'application/json')

            if edit_encounter is not None:
                new_encounter_values = edit_encounter.to_dict()
                new_encounter_values.update(encounter)
                edit_encounter.update_from_dict(new_encounter_values)

    # editing morphometrics
    morphometrics = data.get('morphometrics')
    if morphometrics is not None:
        morphometrics_id = morphometrics.get('morphometrics_id')
        if morphometrics_id is not None:
            edit_morphometrics = db.session.query(Morphometrics).filter(Morphometrics.morphometrics_id == morphometrics_id).first()
            if edit_morphometrics is not None:
                new_morphometrics_values = edit_morphometrics.to_dict()
                new_morphometrics_values.update(morphometrics)
                edit_morphometrics.update_from_dict(new_morphometrics_values)

    # editing samples
    samples = data.get('samples')
    if samples is not None:
        for s in samples:
            sample_id = s.get('sample_id')
            if sample_id is not None:
                edit_sample = db.session.query(Sample).filter(Sample.sample_id == sample_id).first()
                if edit_sample is not None:
                    new_sample_values = edit_sample.to_dict()
                    new_sample_values.update(s)
                    edit_sample.update_from_dict(new_sample_values)

    # editing tags
    tags = data.get('tags')
    if tags is not None:
        encounter_id = tags[0]['encounter_id']
        edit_encounter = db.session.query(BeachEncounter).filter(BeachEncounter.encounter_id == encounter_id).first()
        for t in tags:
            tag_id = t.get('tag_id')
            if tag_id is not None:
                edit_tag = db.session.query(Tag).filter(Tag.tag_id == tag_id).first()
                if edit_tag is not None:
                    old_tag_number = edit_tag.tag_number
                    new_tag_number = t.get('tag_number')
                    # case handling to update tags assoc. w/encounter (as opposed to all tags assoc. w/turtle)
                    if new_tag_number is not None and old_tag_number != new_tag_number:
                        j = 0
                        old_tag = edit_encounter.tag1
                        if old_tag == old_tag_number:
                            setattr(edit_encounter,'tag1',new_tag_number)
                        else:
                            old_tag = edit_encounter.tag2
                            if old_tag == old_tag_number:
                                setattr(edit_encounter,'tag2',new_tag_number)
                            else:
                                old_tag = edit_encounter.tag3
                                if old_tag == old_tag_number:
                                    setattr(edit_encounter,'tag3',new_tag_number)
                    new_tag_values = edit_tag.to_dict()
                    new_tag_values.update(t)
                    edit_tag.update_from_dict(new_tag_values, error_on_extra_keys=False, drop_extra_keys=True)
    
    # editing clutch
    clutches = data.get('clutches')
    if clutches is not None:
        for c in clutches:
            clutch_id = c.get('clutch_id')
            if clutch_id is not None:
                edit_clutch = db.session.query(Clutch).filter(Clutch.clutch_id == clutch_id).first()
                if edit_clutch is not None:
                    new_clutch_values = edit_clutch.to_dict()
                    new_clutch_values.update(c)
                    edit_clutch.update_from_dict(new_clutch_values)

    db.session.commit()

    return {'message':'Beach encounter edited successfully'}

# deleting a beach encounter + casacdes thru all assoc. tables
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