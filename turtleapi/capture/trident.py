from turtleapi import db
from turtleapi.models.turtlemodels import (TridentEncounter, Encounter, Turtle, Tag,
                                           Morphometrics, Sample, TridentMetadata,
                                           Metadata, Net, IncidentalCapture)
from datetime import datetime, timedelta
import json
from turtleapi.capture.util import find_turtle_from_tags, date_handler, get_miniquery_filters, generate_miniquery_queries
from flask import jsonify, Response
import random # we can remove this when we're done and don't do the manual test insertions anymore

def mini_query_trident(data):
    filters = get_miniquery_filters(data)
 
    if filters['metadata_date'] is not None and filters['metadata_id'] is None: # Overwrite metadata_id only if it doesn't exist and we have a metadata_date asked
        filters['metadata_id'] = db.session.query(TridentMetadata.metadata_id).filter(TridentMetadata.metadata_date == filters['metadata_date']).first()
        if filters['metadata_id'] is None:  # If date doesn't match anything, make sure we return no results
            filters['metadata_id'] = -1

    queries = generate_miniquery_queries(filters, TridentEncounter)

    result = db.session.query(TridentEncounter.encounter_id, TridentEncounter.encounter_date, Turtle.turtle_id, Turtle.species).filter(*queries, Turtle.turtle_id==Encounter.turtle_id).all() # returns list of result objects
    final_result = [x._asdict() for x in result] # json.dumps() strips the name of the field... convert to dict and json.dumps() saves it

    return Response(json.dumps(final_result, default = date_handler),mimetype = 'application/json')

def query_trident(data):

    # Filters
    FILTER_encounter_id = data.get('encounter_id')

    # Error out if no encounter_id
    if FILTER_encounter_id is None:
        print("error: no encounter id provided to full trident query")
        return {'error': 'no encounter id provided to full trident query'}
    
    # Build queries
    queries = []

    queries.append(Encounter.encounter_id == FILTER_encounter_id)
    queries.append(Encounter.type == "trident")

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

def query_trident_metadata(data):
    ### FILTERS
    FILTER_metadata_id = data.get('metadata_id', '')
    FILTER_metadata_date = data.get('metadata_date', '')
    FILTER_metadata_type = "trident"
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

def insert_trident(data):
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
        encounter = TridentEncounter.new_from_dict(data2['encounters'], error_on_extra_keys=False, drop_extra_keys=True)
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
        encounter = TridentEncounter.new_from_dict(data2['encounters'], error_on_extra_keys=False, drop_extra_keys=True)
        encounter.metadata_id = metadata_id
        del data2['encounters']
        turtle = Turtle.new_from_dict(data2, error_on_extra_keys=False, drop_extra_keys=True)

    encounter.turtle = turtle
    db.session.add(encounter)
    db.session.commit()

    return {'message': 'no errors'}

def insert_trident_metadata(data):
    metadata = TridentMetadata.new_from_dict(data, error_on_extra_keys=False, drop_extra_keys=True)
    db.session.add(metadata)
    db.session.commit()

    return {'message': 'no errors'}

def edit_trident(data):
    turtle = data.get('turtle')
    if turtle is not None:
        turtle_id = turtle.get('turtle_id')
        if turtle_id is not None:
            edit_turtle = db.session.query(Turtle).filter(Turtle.turtle_id == turtle_id).first()
            if edit_turtle is not None:
                new_turtle_values = edit_turtle.to_dict()       # Get current DB values
                new_turtle_values.update(turtle)                # Update with any new values from incoming JSON
                edit_turtle.update_from_dict(new_turtle_values) # Update DB entry

    encounter = data.get('encounter')
    if encounter is not None:
        encounter_id = encounter.get('encounter_id')
        if encounter_id is not None:
            edit_encounter = db.session.query(TridentEncounter).filter(TridentEncounter.encounter_id == encounter_id).first()
            # return Response(json.dumps(edit_encounter.to_dict(max_nesting=5), default = date_handler),mimetype = 'application/json')

            if edit_encounter is not None:
                new_encounter_values = edit_encounter.to_dict()
                new_encounter_values.update(encounter)
                edit_encounter.update_from_dict(new_encounter_values)

    morphometrics = data.get('morphometrics')
    if morphometrics is not None:
        morphometrics_id = morphometrics.get('morphometrics_id')
        if morphometrics_id is not None:
            edit_morphometrics = db.session.query(Morphometrics).filter(Morphometrics.morphometrics_id == morphometrics_id).first()
            if edit_morphometrics is not None:
                new_morphometrics_values = edit_morphometrics.to_dict()
                new_morphometrics_values.update(morphometrics)
                edit_morphometrics.update_from_dict(new_morphometrics_values)

    tags = data.get('tags')
    if tags is not None:
        for t in tags:
            tag_id = t.get('tag_id')
            if tag_id is not None:
                edit_tag = db.session.query(Tag).filter(Tag.tag_id == tag_id).first()
                if edit_tag is not None:
                    new_tag_values = edit_tag.to_dict()
                    new_tag_values.update(t)
                    edit_tag.update_from_dict(new_tag_values)

    db.session.commit()

    return {'message':'Trident encounter edited successfully'}

def edit_trident_metadata(data):
    metadata = data.get('metadata')
    if metadata is not None:
        metadata_id = metadata.get('metadata_id')
        if metadata_id is not None:
            edit_metadata = db.session.query(TridentMetadata).filter(TridentMetadata.metadata_id == metadata_id).first()

            if edit_metadata is not None:
                new_metadata_values = edit_metadata.to_dict()
                new_metadata_values.update(metadata)
                edit_metadata.update_from_dict(new_metadata_values)

    incidental_captures = data.get('incidental_captures')
    if incidental_captures is not None:
        for ic in incidental_captures:
            incidental_capture_id = ic.get('incidental_capture_id')
            if incidental_capture_id is not None:
                edit_incidental_capture = db.session.query(IncidentalCapture).filter(IncidentalCapture.incidental_capture_id == incidental_capture_id).first()
                if edit_incidental_capture is not None:
                    new_incidental_capture_values = edit_incidental_capture.to_dict()
                    new_incidental_capture_values.update(ic)
                    edit_incidental_capture.update_from_dict(new_incidental_capture_values)
    
    nets = data.get('nets')
    if nets is not None:
        for n in nets:
            net_id = n.get('net_id')
            if net_id is not None:
                edit_net = db.session.query(Net).filter(Net.net_id == net_id).first()
                if edit_net is not None:
                    new_net_values = edit_net.to_dict()
                    new_net_values.update(n)
                    edit_net.update_from_dict(new_net_values)

    db.session.commit()

    return {'message':'Trident metadata edited successfully'}

def delete_trident(data):
    encounter_id = data.get('encounter_id')

    if encounter_id is None:
        return {'error': 'TridentEncounter delete input is in invalid format'}
    
    edit_encounter = db.session.query(TridentEncounter).filter(TridentEncounter.encounter_id == encounter_id).first()

    if edit_encounter is not None:
        db.session.delete(edit_encounter)   # Get current DB values
        db.session.commit()                 # commit changes to DB

        return {'message':'Trident encounter deleted successfully'}

    return {'message':'No matching trident encounters found'}

def delete_trident_metadata(data):
    metadata_id = data.get('metadata_id')

    if metadata_id is None:
        return {'error': 'TridentMetadata delete input is in invalid format'}
    
    edit_metadata = db.session.query(TridentMetadata).filter(TridentMetadata.metadata_id == metadata_id).first()

    if edit_encounter is not None:
        encounters = db.session.query(Encounter).filter(Encounter.metadata_id == metadata_id).first()
        if encounters is not None:
            return {'error': 'There are trident encounters associated with that metadata id'}
        
        db.session.delete(edit_encounter)   # Get current DB values
        db.session.commit()                 # commit changes to DB

        return {'message':'Trident metadata deleted successfully'}

    return {'message':'No matching trident metadatas found'}
