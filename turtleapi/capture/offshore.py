from turtleapi import db
from turtleapi.models.turtlemodels import (OffshoreEncounter, Encounter, Turtle, Tag,
                                           Morphometrics, Sample, OffshoreMetadata,
                                           Metadata)
from datetime import datetime, timedelta
import json
from turtleapi.capture.util import find_turtle_from_tags, date_handler, get_miniquery_filters, generate_miniquery_queries
from flask import jsonify, Response
import random # we can remove this when we're done and don't do the manual test insertions anymore

def mini_query_offshore(data):
    filters = get_miniquery_filters(data)
 
    # below, using "metadata_date" to keep consistency -> capture_date
    if filters['metadata_date'] is not None and filters['metadata_id'] is None: # Overwrite metadata_id only if it doesn't exist and we have a metadata_date asked
        filters['metadata_id'] = db.session.query(OffshoreMetadata.metadata_id).filter(OffshoreMetadata.capture_date == filters['metadata_date']).all()
        if filters['metadata_id'] is None:  # If date doesn't match anything, make sure we return no results
            filters['metadata_id'] = -1

    queries = generate_miniquery_queries(filters, OffshoreEncounter)

    result = db.session.query(OffshoreEncounter.encounter_id, Turtle.turtle_id, Turtle.species).filter(*queries, Turtle.turtle_id==Encounter.turtle_id).all() # returns list of result objects
    final_result = [x._asdict() for x in result] # json.dumps() strips the name of the field... convert to dict and json.dumps() saves it

    return Response(json.dumps(final_result, default = date_handler),mimetype = 'application/json')

def query_offshore(data):

    # Filters
    FILTER_encounter_id = data.get('encounter_id')

    # Error out if no encounter_id
    if FILTER_encounter_id is None:
        print("error: no encounter id provided to full offshore query")
        return {'error': 'no encounter id provided to full offshore query'}
    
    # Build queries
    queries = []

    queries.append(Encounter.encounter_id == FILTER_encounter_id)
    queries.append(Encounter.type == "offshore")

    # Grab turtles
    result = db.session.query(OffshoreMetadata, Turtle.species).filter(*queries, Encounter.metadata_id==OffshoreMetadata.metadata_id, Turtle.turtle_id==Encounter.turtle_id).first()

    if result is None:
        return {'error': 'No encounter with that ID exists'}

    # Add species
    result_encounter = result[0].to_dict(max_nesting=5)
    result_encounter['species'] = result[1]
    
    # Grab tags
    tags = db.session.query(Tag).filter(Tag.turtle_id==result_encounter['encounters'][0]['turtle_id']).all()
    result_encounter['encounters'][0]['tags'] = [x.to_dict() for x in tags]

    return Response(json.dumps(result_encounter, default = date_handler),mimetype = 'application/json')

def insert_offshore(data): # includes offshore metadata
    data2 = {}
    data2['metadata'] = data
    data2['turtle'] = {}
    data2['turtle']['tags'] = data2['metadata']['encounters']['tags']
    del data2['metadata']['encounters']['tags']
    data2['turtle']['species'] = data2['metadata']['encounters']['species']
    del data2['metadata']['encounters']['species']
    data2['metadata']['encounters']['morphometrics'] = [data2['metadata']['encounters']['morphometrics']]

    # handling turtle
    turtle = find_turtle_from_tags(data2['turtle']['tags'])
    if turtle is not None:
        data2['metadata']['encounters']['capture_type'] = "recap"

        compare_tags = db.session.query(Tag).filter(Tag.turtle_id==turtle.turtle_id,Tag.active==True)
        # updating existing tags
        for c in compare_tags:
            flag = False
            i = 0
            for i in range(len(data2['turtle']['tags'])):
                if c.tag_number == data2['turtle']['tags'][i]['tag_number']:
                    setattr(c,'tag_scars',data2['turtle']['tags'][i]['tag_scars'])
                    flag = True
                    del data2['turtle']['tags'][i]
                    break
                i = i + 1
            if flag == False:
                setattr(c,'active',False)
        # adding new tags
        for t in data2['turtle']['tags']:
            tag = Tag.new_from_dict(t, error_on_extra_keys=False, drop_extra_keys=True)
            tag.turtle_id = turtle.turtle_id
            db.session.add(tag)
        del data2['turtle']
    else:
        turtle = Turtle.new_from_dict(data2['turtle'], error_on_extra_keys=False, drop_extra_keys=True)
        del data2['turtle']
        data2['metadata']['encounters']['capture_type'] = "new"
    
    encounter = OffshoreEncounter.new_from_dict(data2['metadata']['encounters'], error_on_extra_keys=False, drop_extra_keys=True)
    del data2['metadata']['encounters']
    encounter.turtle = turtle
    metadata = OffshoreMetadata.new_from_dict(data2['metadata'], error_on_extra_keys=False, drop_extra_keys=True)
    del data2['metadata']
    encounter.metadata = metadata
    db.session.add(encounter)
    db.session.add(metadata)
    db.session.commit()

    return {'message': 'no errors'}

def edit_offshore(data):
    return {'message': 'WIP'}
    # encounter_id = data['metadata']['encounters'][0].get('encounter_id')

    # if encounter_id is None:
    #     return {'error': 'OffshoreEncounter edit input is in invalid format'}
    
    # edit_encounter = db.session.query(OffshoreMetadata, Turtle.species, Tag).filter(OffshoreEncounter.encounter_id == encounter_id,
    #                                                                                 OffshoreMetadata.metadata_id == OffshoreEncounter.metadata_id,
    #                                                                                 Turtle.turtle_id == OffshoreEncounter.turtle_id,
    #                                                                                 Tag.turtle_id == Turtle.turtle_id).first()

    # if edit_encounter is not None:
    #     new_encounter_values = {}
    #     new_encounter_values['metadata'] = edit_encounter[0].to_dict(max_nesting=5) # Get current DB values
    #     new_encounter_values['species'] = edit_encounter[1]
    #     new_encounter_values.update(tags = edit_encounter[2].to_dict())
    #     # return new_encounter_values
    #     new_encounter_values.update(data)                       # Update with any new values from incoming JSON
    #     edit_encounter[0].update_from_dict(new_encounter_values['metadata'], error_on_extra_keys=False, drop_extra_keys=True)   # Update DB entry
    #     edit_encounter[2].update_from_dict(new_encounter_values['tags'])
        
    #     db.session.commit()                                     # commit changes to DB

    #     return {'message':'Offshore encounter edited successfully'}

    # return {'message':'No matching offshore encounters found'}

def delete_offshore(data):
    metadata_id = data.get('metadata_id')

    if metadata_id is None:
        return {'error': 'OffshoreMetadata delete input is in invalid format'}
    
    edit_metadata = db.session.query(OffshoreMetadata).filter(OffshoreMetadata.metadata_id == metadata_id).first()

    if edit_metadata is not None:
        db.session.delete(edit_metadata)   # Get current DB values
        db.session.commit()                 # commit changes to DB

        return {'message':'Offshore metadata deleted successfully'}

    return {'message':'No matching offshore metadata found'}