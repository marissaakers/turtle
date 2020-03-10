from turtleapi import db
from turtleapi.models.turtlemodels import (LagoonEncounter, Encounter, Turtle, Tag,
                                           Morphometrics, Sample, Metadata, LagoonMetadata, Net,
                                           IncidentalCapture)
from datetime import datetime, timedelta
import json
from turtleapi.capture.util import find_turtle_from_tags, date_handler, get_miniquery_filters, generate_miniquery_queries
from flask import jsonify, Response

def mini_query_lagoon(data):
    filters = get_miniquery_filters(data)
 
    if filters['metadata_date'] is not None and filters['metadata_id'] is None: # Overwrite metadata_id only if it doesn't exist and we have a metadata_date asked
        filters['metadata_id'] = db.session.query(LagoonMetadata.metadata_id).filter(LagoonMetadata.metadata_date == filters['metadata_date']).first()
        if filters['metadata_id'] is None:  # If date doesn't match anything, make sure we return no results
            filters['metadata_id'] = -1

    queries = generate_miniquery_queries(filters, LagoonEncounter)

    result = db.session.query(LagoonEncounter.encounter_id, LagoonEncounter.encounter_date, Turtle.turtle_id, Turtle.species).filter(*queries, Turtle.turtle_id==Encounter.turtle_id).all() # returns list of result objects
    final_result = [x._asdict() for x in result] # json.dumps() strips the name of the field... convert to dict and json.dumps() saves it

    return Response(json.dumps(final_result, default = date_handler),mimetype = 'application/json')

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

def query_lagoon_metadata(data):
    ### FILTERS
    FILTER_metadata_id = data.get('metadata_id', '')
    FILTER_metadata_date = data.get('metadata_date', '')
    FILTER_metadata_type = "lagoon"
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

def insert_lagoon_metadata(data):
    metadata = LagoonMetadata.new_from_dict(data, error_on_extra_keys=False, drop_extra_keys=True)
    db.session.add(metadata)
    db.session.commit()

    return {'message': 'no errors'}

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

def edit_lagoon_metadata(data):
    metadata_id = data.get('metadata_id')

    if metadata_id is None:
        return {'error': 'LagoonMetadata edit input is in invalid format'}
    
    edit_metadata = db.session.query(LagoonMetadata).filter(LagoonMetadata.metadata_id == metadata_id).first()

    if edit_metadata is not None:
        new_metadata_values = edit_metadata.to_dict()           # Get current DB values
        new_metadata_values.update(data)                        # Update with any new values from incoming JSON
        edit_metadata.update_from_dict(new_metadata_values)     # Update DB entry
        
        db.session.commit()                                     # commit changes to DB

        return {'message':'Lagoon metadata edited successfully'}

    return {'message':'No matching lagoon metadatas found'}

def delete_lagoon(data):
    encounter_id = data.get('encounter_id')

    if encounter_id is None:
        return {'error': 'LagoonEncounter delete input is in invalid format'}
    
    edit_encounter = db.session.query(LagoonEncounter).filter(LagoonEncounter.encounter_id == encounter_id).first()

    if edit_encounter is not None:
        db.session.delete(edit_encounter)   # Get current DB values
        db.session.commit()                 # commit changes to DB

        return {'message':'Lagoon encounter deleted successfully'}

    return {'message':'No matching lagoon encounters found'}

def delete_lagoon_metadata(data):
    metadata_id = data.get('metadata_id')

    if metadata_id is None:
        return {'error': 'LagoonMetadata delete input is in invalid format'}
    
    edit_metadata = db.session.query(LagoonMetadata).filter(LagoonMetadata.metadata_id == metadata_id).first()

    if edit_metadata is not None:
        db.session.delete(edit_metadata)   # Get current DB values
        db.session.commit()                 # commit changes to DB

        return {'message':'Lagoon metadata deleted successfully'}

    return {'message':'No matching lagoon metadatas found'}