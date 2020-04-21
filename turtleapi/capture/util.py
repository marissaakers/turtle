from turtleapi import db
from sqlalchemy.orm import with_polymorphic
from turtleapi.models.turtlemodels import (Turtle, Tag, Encounter, LagoonEncounter, TridentEncounter, 
    BeachEncounter, OffshoreEncounter, OtherEncounter)
import json
from flask import jsonify, make_response, redirect
import requests, os, boto3 # could remove this (maybe others?) if i move pdf to its own file?
from turtleapi import app
import base64
import io
from datetime import date, timedelta

# Match one turtle
def find_turtle_from_tags(tags):
    # taglist = []
    
    # for t in tags:
    #     taglist.append(t['tag_number'])

    # turtle = Turtle.query.filter(Tag.tag_number.in_(taglist)).first()
    # if turtle is not None:
    #     turtle_schema = TurtleSchema()
    #     return turtle_schema.dump(turtle)
    # return None

    for t in tags:
        res = db.session.query(Tag).filter(Tag.tag_number==t['tag_number']).first()
        if res is not None:
            turtle = db.session.query(Turtle).filter(Turtle.turtle_id==res.turtle_id).first()
            return turtle
    return None

# Match all turtles
def find_turtles_from_tags(tags):
    #turtle_ids = Tag.query.filter(Tag.tag_number.in_(tags)).all() #.distinct()
    #turtle_ids = Tag.query.filter(Tag.tag_number.in_(tags)).distinct()
    # turtle_ids = Tag.query.distinct(Tag.turtle_id).filter(Tag.tag_number.in_(tags)).all()
    #turtle_ids = Tag.query.with_entities(Tag.turtle_id).distinct(Tag.turtle_id).filter(Tag.tag_number.in_(tags)).all() # doesn't work?
    turtle_ids = db.session.query(Tag.turtle_id).filter(Tag.tag_number.in_(tags)).all()
    
    taglist = []
    if turtle_ids is not None:
        for x in turtle_ids:
            for y in x:
                taglist.append(y)
        return taglist
    return None

def return_tag_status(tags):
    print(tags)
    NO_TAGS_SENT = 'Please enter at least one tag to check tag status.'
    TAGS_NOT_FOUND = 'Tag(s) not found in database; '
    TAGS_FOUND = 'Tag(s) found in database; '
    NEW_ENCOUNTER = 'this is a new encounter.'
    STRANGE_ENCOUNTER = 'this is a strange encounter.'
    RECAP_ENCOUNTER = 'this is a recapture encounter.'
    STRANGE_RECAP_ENCOUNTER = 'this is a strange recapture encounter.'

    if len(tags) == 0:
        return {'message': NO_TAGS_SENT}

    strange_encounter = False
    recapture = False
    id_list = {}
    multiple_turtle_indexes = []

    for tag in tags:
        turtle_id = db.session.query(Tag.turtle_id).filter(Tag.tag_number==tag['tag_number']).first()
        if turtle_id is not None:
            recapture = True
            id_list[tag['tag_number']] = turtle_id[0]
        else:
            if tag['new'] == False:
                strange_encounter = True

    if len(id_list) == 0:
        return {'message': TAGS_NOT_FOUND + (STRANGE_ENCOUNTER if strange_encounter else NEW_ENCOUNTER)}
    elif len(id_list) > 1:
        # find multiple turtles
        for i in range (0, len(id_list)-1):
            for j in range (1, len(id_list)):
                tag1 = tags[i]["tag_number"]
                tag2 = tags[j]["tag_number"]
                if id_list[tag1] != id_list[tag2]:
                    multiple_turtle_indexes.append(i)
                    multiple_turtle_indexes.append(j)
                    break
    # if multiple turtles, tell the user
    if len(multiple_turtle_indexes) > 0:
        tag1 = tags[multiple_turtle_indexes[0]]['tag_number']
        tag2 = tags[multiple_turtle_indexes[1]]['tag_number']
        return {'message': 'Error: tag number ' + tag1 + ' belongs to '
                + 'turtle id ' + str(id_list[tag1]) + ', while tag number ' + tag2
                + ' belongs to turtle id ' + str(id_list[tag2]) + '. '
                + 'Please double check the tag numbers.'}

    # We can return a normal response if we get to this point
    turtle_id = id_list[tags[0]['tag_number']]
    # no tags found
    if turtle_id is None:
        return {'message': TAGS_NOT_FOUND + '' + (STRANGE_ENCOUNTER if strange_encounter else NEW_ENCOUNTER)}
    # at least one tag found so it's a recap
    return {'message': TAGS_FOUND + '' + (STRANGE_ENCOUNTER if strange_encounter else RECAP_ENCOUNTER)}

def return_tag_status_two(tags):
    strange_encounter = False
    recapture = False

    for tag in tags:
        turtle_id = db.session.query(Tag.turtle_id).filter(tag_number==tag['tag_number']).first()
        if turtle_id is not None:
            recapture = True
        else:
            if tag['new'] == False:
                strange_encounter = True

    return {'strange_encounter': strange_encounter, 'recapture': recapture}


# For editing, insert any new tags
# WIP & untested 
# def insert_new_tags(turtle_id, tags):
#     turtle_result = Tag.query.filter(Tag.turtle_id == turtle_id)
    
#     if turtle_result is not None:
#         tag_schema = TagSchema()
#         turtle_result_dump = tag_schema.dump(turtle_result, many=True)
#         turtle_tag_list = [d['tag_number'] for d in turtle_result_dump]
#         for t in tags:
#             if t not in turtle_tag_list:
#                 new_tag = Tag(
#                 turtle=turtle_id,
#                 tag_number=t,
#                 location="DEBUG",
#                 active=tag['active'],
#                 tag_type=tag['tag_type'] #grrr
#             )
        
def my_custom_serializer(value, **kwargs):
    filter_fields = kwargs.pop("filter_fields", None)
    result = {}
    for field in filter_fields:
        result[field] = value.get(field, None)

    return result
#    return json.dumps(result)

def date_handler(obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()

def get_miniquery_filters(data):

    filters = {}
    filters['tags'] = data.get('tags')
    filters['turtle_id'] = data.get('turtle_id')
    filters['species'] = data.get('species')    # Only match this species

    filters['encounter_id'] = data.get('encounter_id')
    filters['encounter_date_start'] = data.get('encounter_date_start')  # Match between FILTER_DATE_START and FILTER_DATE_END
    filters['encounter_date_end'] = data.get('encounter_date_end')

    filters['entered_by'] = data.get('entered_by')
    filters['verified_by'] = data.get('verified_by')
    filters['investigated_by'] = data.get('investigated_by')

    filters['metadata_id'] = data.get('metadata_id')
    filters['metadata_ids'] = data.get('metadata_ids')
    filters['metadata_date'] = data.get('metadata_date')
    filters['capture_date'] = data.get('capture_date')
    
    # If tags, find IDs and search by ID
    filters['turtle_ids'] = None
    if filters['tags'] is not None:
        filters['turtle_ids'] = find_turtles_from_tags(filters['tags'])
    if filters['turtle_id'] is not None:
        if filters['tags'] is not None:
            filters['turtle_ids'].append(filters['turtle_id'])
        else:
            filters['turtle_ids'] = [filters['turtle_id'],]

    return filters

def generate_miniquery_queries(filters, enc):

    queries = []

    if filters['turtle_ids'] is not None:
        queries.append(Encounter.turtle_id.in_(filters['turtle_ids']))
    if filters['encounter_id'] is not None:
        queries.append(Encounter.encounter_id == filters['encounter_id'])
    if filters['encounter_date_start'] is not None and enc is not OffshoreEncounter:
        queries.append(enc.encounter_date >= filters['encounter_date_start'])
    else:
        if enc is not OffshoreEncounter:
            queries.append(enc.encounter_date >= (date.today() - timedelta(365)))  # If no start date, only do 1 year
    if filters['encounter_date_end'] is not None and enc is not OffshoreEncounter:
        queries.append(enc.encounter_date <= filters['encounter_date_end'])
    if filters['entered_by'] is not None:
        queries.append(enc.entered_by.contains(filters['entered_by']))
    if filters['verified_by'] is not None:
        queries.append(enc.verified_by.contains(filters['verified_by']))
    if filters['investigated_by'] is not None:
        queries.append(enc.investigated_by.contains(filters['investigated_by']))
    if filters['species'] is not None:
        queries.append(Turtle.species.contains(filters['species']))
    if filters['metadata_id'] is not None:
        queries.append(Encounter.metadata_id == filters['metadata_id'])
    if filters['metadata_ids'] is not None:
        queries.append(Encounter.metadata_id.in_(filters['metadata_ids']))

    return queries

# boto3 head_object is VERY slow
# Faster way to check if a file exists on s3
def check_if_s3_file_exists(client, bucket, key):
    response = client.list_objects_v2(
        Bucket=bucket,
        Prefix=key,
    )
    for obj in response.get('Contents', []):
        if obj['Key'] == key:
            return True
    
    return False


def get_file(data):
    encounter_id = data.get('encounter_id')
    pdf_filename = data.get('pdf_filename')
    img_filename = data.get('img_filename')

    pdf = None
    if pdf_filename == '' or pdf_filename:
        pdf = True
    elif img_filename == '' or img_filename:    
        pdf = False

    if encounter_id is None or pdf is None:
        return {'error': 'File get query missing encounter_id or filename'}

    encounter_result = db.session.query(Encounter).get(encounter_id)

    if encounter_result is None:
        return {'error': 'No such encounter_id exists'}

    if pdf and encounter_result.pdf_filename is None:
        return {'message': 'No PDF file attached to this encounter'}
    if not pdf and encounter_result.img_filename is None:
        return {'message': 'No image file attached to this encounter'}

    s3 = boto3.client('s3', aws_access_key_id=app.config['ACCESS_KEY_ID'], aws_secret_access_key=app.config['SECRET_ACCESS_KEY'])

    url = None
    if pdf:
        url = s3.generate_presigned_url('get_object', Params = {'Bucket': app.config['S3_BUCKET'], 'Key': encounter_result.pdf_filename}, ExpiresIn = 3600)
        fname = encounter_result.pdf_filename
    else:
        url = s3.generate_presigned_url('get_object', Params = {'Bucket': app.config['S3_BUCKET'], 'Key': encounter_result.img_filename}, ExpiresIn = 3600)
        fname = encounter_result.img_filename
    
    if not check_if_s3_file_exists(s3, app.config['S3_BUCKET'], fname):
        return {'message': 'No such file attached to this encounter'}
        #s3.head_object(Bucket=app.config['S3_BUCKET'], Key=fname) # Very slow for some reason

    #return redirect(url, code=302)
    return {'url': url}

def put_file(data):
    encounter_id = data.get('encounter_id')
    pdf_filename = data.get('pdf_filename')
    img_filename = data.get('img_filename')
    
    pdf = None
    if pdf_filename:
        pdf = True
    elif img_filename:    
        pdf = False
    
    if pdf_filename == '':
        return {'error': 'File put query missing PDF filename'}
    elif img_filename == '':
        return {'error': 'File put query missing img filename'}

    if encounter_id is None or pdf is None:
        return {'error': 'File put query missing encounter_id or filetype'}

    encounter_result = db.session.query(Encounter).get(encounter_id)

    if encounter_result is None:
        return {'error': 'No such encounter_id exists'}

    if pdf:
        conflicting_filename_check_pdf = db.session.query(Encounter).filter(Encounter.pdf_filename == pdf_filename).first()
        if (conflicting_filename_check_pdf is not None) and (conflicting_filename_check_pdf.encounter_id != encounter_id):
            return {'error': 'Editing encounter_id ' + str(encounter_id) + ' but encounter_id ' + 
                    str(conflicting_filename_check_pdf.encounter_id) + ' has this pdf_filename'}

    else:
        conflicting_filename_check_img = db.session.query(Encounter).filter(Encounter.pdf_filename == img_filename).first()
        if (conflicting_filename_check_img is not None) and (conflicting_filename_check_img.encounter_id != encounter_id):
            return {'error': 'Editing encounter_id ' + str(encounter_id) + ' but encounter_id ' + 
                    str(conflicting_filename_check_img.encounter_id) + ' has this img_filename'}

    old_filename = None
    if pdf:
        old_filename = encounter_result.pdf_filename
    else:
        old_filename = encounter_result.img_filename

    s3 = boto3.client('s3', aws_access_key_id=app.config['ACCESS_KEY_ID'], aws_secret_access_key=app.config['SECRET_ACCESS_KEY'], region_name='us-east-1')
    
    if old_filename is not None:    # If old file exists, delete old file before uploading new file
        try:
            s3.delete_object(Bucket=app.config['S3_BUCKET'], Key=old_filename)
        except:
            print("Tried to delete nonexistent object")
            
    try:
        if pdf:
            pdf_filename = str(encounter_result.encounter_id) + "p-" + pdf_filename
            #s3.upload_fileobj(fileobj, app.config['S3_BUCKET'], pdf_filename, ExtraArgs={"ContentType": 'pdf'})
            encounter_result.pdf_filename = pdf_filename
            db.session.commit()
            return s3.generate_presigned_post(Bucket=app.config['S3_BUCKET'], Key=pdf_filename, ExpiresIn=3600)
            #return s3.generate_presigned_url(Bucket=app.config['S3_BUCKET'], Key=pdf_filename, ExpiresIn=3600)
            #return s3.generate_presigned_url('put_object', Params={'Bucket':app.config['S3_BUCKET'],'Key':pdf_filename}, ExpiresIn=3600, HttpMethod='PUT', Content-Type: 'application/octet-stream')
        else:
            img_filename = str(encounter_result.encounter_id) + "i-" + img_filename
            #s3.upload_fileobj(fileobj, app.config['S3_BUCKET'], img_filename)
            encounter_result.img_filename = img_filename
            db.session.commit()
            return s3.generate_presigned_post(Bucket=app.config['S3_BUCKET'], Key=img_filename, ExpiresIn=3600)
            #return s3.generate_presigned_url('put_object', Params={'Bucket':app.config['S3_BUCKET'],'Key':img_filename}, ExpiresIn=3600, HttpMethod='PUT', Content-Type: 'application/octet-stream')

    except Exception as e:
        return {'error': str(e)}

    return {'message': 'file posted successfully'}