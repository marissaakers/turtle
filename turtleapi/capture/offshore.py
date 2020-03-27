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
            filters['metadata_id'] = [-1,]

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

def edit_offshore(data):                         # commit changes to DB
    metadata = data.get('metadata')
    if metadata is not None:
        metadata_id = metadata.get('metadata_id')
        if metadata_id is not None:
            edit_metadata = db.session.query(OffshoreMetadata).filter(OffshoreMetadata.metadata_id == metadata_id).first()

            if edit_metadata is not None:
                new_metadata_values = edit_metadata.to_dict()
                new_metadata_values.update(metadata)
                edit_metadata.update_from_dict(new_metadata_values)
    
    encounter = data.get('encounter')
    if encounter is not None:
        encounter_id = encounter.get('encounter_id')
        if encounter_id is not None:
            edit_encounter = db.session.query(OffshoreEncounter).filter(OffshoreEncounter.encounter_id == encounter_id).first()
            if edit_encounter is not None:
                new_encounter_values = edit_encounter.to_dict()
                new_encounter_values.update(encounter)
                edit_encounter.update_from_dict(new_encounter_values)

    turtle = data.get('turtle')
    if turtle is not None:
        turtle_id = turtle.get('turtle_id')
        if turtle_id is not None:
            edit_turtle = db.session.query(Turtle).filter(Turtle.turtle_id == turtle_id).first()
            if edit_turtle is not None:
                new_turtle_values = edit_turtle.to_dict()       # Get current DB values
                new_turtle_values.update(turtle)                # Update with any new values from incoming JSON
                edit_turtle.update_from_dict(new_turtle_values) # Update DB entry

    morphometrics = data.get('morphometrics')
    if morphometrics is not None:
        morphometrics_id = morphometrics.get('morphometrics_id')
        if morphometrics_id is not None:
            edit_morphometrics = db.session.query(Morphometrics).filter(Morphometrics.morphometrics_id == morphometrics_id).first()
            if edit_morphometrics is not None:
                new_morphometrics_values = edit_morphometrics.to_dict()
                new_morphometrics_values.update(morphometrics)
                edit_morphometrics.update_from_dict(new_morphometrics_values)

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
    
    return {'message':'Offshore encounter edited successfully'}

def delete_offshore(data):
    metadata_id = data.get('metadata_id')
    encounter_id = data.get('encounter_id')

    if metadata_id is None and encounter_id is None:
        return {'error': 'Offshore delete input is in invalid format'}
        
    if metadata_id is None:
        encounter_query = db.session.query(OffshoreEncounter, OffshoreEncounter.metadata_id).filter(OffshoreEncounter.encounter_id == encounter_id).first()
        if encounter_query is not None:
            edit_encounter = encounter_query[0]
            metadata_id = encounter_query[1]
        else:
            return {'message':'No matching offshore data found'}
    else:
        edit_encounter = db.session.query(OffshoreEncounter).filter(OffshoreEncounter.metadata_id == metadata_id).first()

    edit_metadata = db.session.query(OffshoreMetadata).filter(OffshoreMetadata.metadata_id == metadata_id).first()

    if edit_metadata is not None:
        db.session.delete(edit_encounter)   # Get current DB values
        db.session.delete(edit_metadata)
        db.session.commit()                 # commit changes to DB
    
        return {'message':'Offshore deleted successfully'}

    return {'message':'No matching offshore data found'}

