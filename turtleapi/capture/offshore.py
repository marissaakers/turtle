from turtleapi import db
from turtleapi.models.turtlemodels import (OffshoreEncounter, Encounter, Turtle, Tag,
                                           Morphometrics, Sample, OffshoreMetadata,
                                           Metadata)
from datetime import datetime, timedelta
import json
from turtleapi.capture.util import find_turtle_from_tags, date_handler, get_miniquery_filters, generate_miniquery_queries
from flask import jsonify, Response
import random # we can remove this when we're done and don't do the manual test insertions anymore

# returns metadata_id, encounter_id, turtle_id, and species assoc. w/offshore encounter
def mini_query_offshore(data):
    filters = get_miniquery_filters(data)
 
    # below, using "metadata_date" to keep consistency -> capture_date
    if filters['metadata_date'] is not None and filters['metadata_id'] is None: # Overwrite metadata_id only if it doesn't exist and we have a metadata_date asked
        filters['metadata_id'] = db.session.query(OffshoreMetadata.metadata_id).filter(OffshoreMetadata.capture_date == filters['metadata_date']).all()
        if filters['metadata_id'] is None:  # If date doesn't match anything, make sure we return no results
            filters['metadata_id'] = [-1,]

    queries = generate_miniquery_queries(filters, OffshoreEncounter)

    result = db.session.query(Metadata.metadata_id, OffshoreEncounter.encounter_id, Turtle.turtle_id, Turtle.species).filter(*queries, Encounter.metadata_id==Metadata.metadata_id, Turtle.turtle_id==Encounter.turtle_id).all() # returns list of result objects
    final_result = [x._asdict() for x in result] # json.dumps() strips the name of the field... convert to dict and json.dumps() saves it

    return Response(json.dumps(final_result, default = date_handler),mimetype = 'application/json')

# returns a complete offshore metadata/encounter (w/morphometrics, turtle information, tags, samples)
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
    result = db.session.query(OffshoreMetadata, Turtle.species, Turtle.sex, Encounter.metadata_id).filter(*queries, Encounter.metadata_id==OffshoreMetadata.metadata_id, Turtle.turtle_id==Encounter.turtle_id).first()

    if result is None:
        return {'error': 'No encounter with that ID exists'}

    # Add species
    result_encounter = result[0].to_dict(max_nesting=4)
    result_encounter['species'] = result[1]
    result_encounter['sex'] = result[2]
    
    # Grab tags
    if (result_encounter['encounters'][0]['tag1'] == result_encounter['encounters'][0]['tag2']):
        tags = db.session.query(Tag).filter(Tag.turtle_id==result_encounter['encounters'][0]['turtle_id']).all()
        result_encounter['encounters'][0]['tags'] = [x.to_dict() for x in tags]
    else:
        taglist = [result_encounter['encounters'][0]['tag1'], result_encounter['encounters'][0]['tag2']]
        tags = db.session.query(Tag).filter(Tag.tag_number.in_(taglist)).all()
        result_encounter['encounters'][0]['tags'] = [x.to_dict() for x in tags]

    # Add metadata_id
    result_encounter['metadata_id'] = result[3]

    return Response(json.dumps(result_encounter, default = date_handler),mimetype = 'application/json')

# inserts offshore metadata/encounter (1-1 relation, not 1-many)
def insert_offshore(data):
    data2 = {}
    data2['metadata'] = data
    data2['turtle'] = {}
    data2['turtle']['tags'] = data2['metadata']['encounters']['tags']
    del data2['metadata']['encounters']['tags']
    data2['turtle']['species'] = data2['metadata']['encounters']['species']
    del data2['metadata']['encounters']['species']
    data2['turtle']['sex'] = data2['metadata']['encounters']['sex']
    del data2['metadata']['encounters']['sex']
    data2['metadata']['encounters']['morphometrics'] = [data2['metadata']['encounters']['morphometrics']]

    # handling tag references in encounter
    j = 0
    tagfield = ['tag1', 'tag2']
    for t in data2['turtle']['tags']:
        data2['metadata']['encounters'][tagfield[j]] = t['tag_number']
        j = j + 1

    # handling turtle
    turtle = find_turtle_from_tags(data2['turtle']['tags'])
    # turtle is a recapture
    if turtle is not None:
        if data2['metadata']['encounters']['capture_type'] != "strange recap":
            data2['metadata']['encounters']['capture_type'] = "recap"

        compare_tags = db.session.query(Tag).filter(Tag.turtle_id==turtle.turtle_id,Tag.active==True)
        # updating existing tags
        for c in compare_tags:
            flag = False
            i = 0
            for i in range(len(data2['turtle']['tags'])):
                if c.tag_number == data2['turtle']['tags'][i]['tag_number']:
                    flag = True
                    del data2['turtle']['tags'][i]
                    break
            if flag == False:
                setattr(c,'active',False)
        # adding new tags
        for t in data2['turtle']['tags']:
            # handling strange tags
            if t['isNew'] == False:
                data2['metadata']['encounters']['capture_type'] = "strange recap"
            tag = Tag.new_from_dict(t, error_on_extra_keys=False, drop_extra_keys=True)
            tag.turtle_id = turtle.turtle_id
            db.session.add(tag)
        del data2['turtle']
    # turtle is a new capture
    else:
        if data2['metadata']['encounters']['capture_type'] != "strange recap":
            data2['metadata']['encounters']['capture_type'] = "new"

        # handling strange tags
        for t in data2['turtle']['tags']:
            if t['isNew'] == False:
                data2['metadata']['encounters']['capture_type'] = "strange recap"

        turtle = Turtle.new_from_dict(data2['turtle'], error_on_extra_keys=False, drop_extra_keys=True)
        del data2['turtle']
    
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

# editing offshore metadata/encounter (along w/assoc. tables)
def edit_offshore(data):
    # editing actual metadata instance
    metadata = data.get('metadata')
    if metadata is not None:
        metadata_id = metadata.get('metadata_id')
        if metadata_id is not None:
            edit_metadata = db.session.query(OffshoreMetadata).filter(OffshoreMetadata.metadata_id == metadata_id).first()

            if edit_metadata is not None:
                new_metadata_values = edit_metadata.to_dict()
                new_metadata_values.update(metadata)
                edit_metadata.update_from_dict(new_metadata_values)
    
    # editing actual encounter instance
    encounter = data.get('encounter')
    if encounter is not None:
        encounter_id = encounter.get('encounter_id')
        if encounter_id is not None:
            edit_encounter = db.session.query(OffshoreEncounter).filter(OffshoreEncounter.encounter_id == encounter_id).first()
            if edit_encounter is not None:
                new_encounter_values = edit_encounter.to_dict()
                new_encounter_values.update(encounter)
                edit_encounter.update_from_dict(new_encounter_values)

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
        edit_encounter = db.session.query(OffshoreEncounter).filter(OffshoreEncounter.encounter_id == encounter_id).first()
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
                    new_tag_values = edit_tag.to_dict()
                    new_tag_values.update(t)
                    edit_tag.update_from_dict(new_tag_values, error_on_extra_keys=False, drop_extra_keys=True)

    db.session.commit()
    
    return {'message':'Offshore encounter edited successfully'}

# deleting offshore metadata/encounter + casacdes thru all assoc. tables
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

