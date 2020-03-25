from turtleapi import db
from sqlalchemy.orm import with_polymorphic
from turtleapi.models.turtlemodels import Turtle, Tag, Encounter, LagoonEncounter, TridentEncounter, BeachEncounter, OffshoreEncounter
import json
from flask import jsonify, make_response, redirect
import requests, os, boto3 # could remove this (maybe others?) if i move pdf to its own file?
from turtleapi import app
import base64
import io

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
    filters['metadata_date'] = data.get('metadata_date')
    
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
    if filters['encounter_date_start'] is not None:
        queries.append(enc.encounter_date >= filters['encounter_date_start'])
    if filters['encounter_date_end'] is not None:
        queries.append(enc.encounter_date <= filters['encounter_date_end'])
    if filters['entered_by'] is not None:
        queries.append(enc.entered_by == filters['entered_by'])
    if filters['verified_by'] is not None:
        queries.append(enc.verified_by == filters['verified_by'])
    if filters['investigated_by'] is not None:
        queries.append(enc.investigated_by == filters['investigated_by'])
    if filters['species'] is not None:
        queries.append(Turtle.species == filters['species'])
    if filters['metadata_id'] is not None:
        queries.append(Encounter.metadata_id.in_(filters['metadata_id']))

    return queries

def get_pdf(data):
    # filename = data.get('filename')

    # if filename is None:
    #     return {'error': 'PDF query missing filename input'}

    # url = 'https://mtrg-files-bucket.s3.amazonaws.com/' + filename + '.pdf'

    # pdf = requests.get(url)
    # if pdf.status_code != 200:
    #     return {'error': 'File does not exist'}

    # response = make_response(pdf.content)
    # response.headers['Content-Type'] = 'application/pdf'
    # response.headers['Content-Disposition'] = 'attachment; filename=report.pdf'
    # return response

    filename = data.get('filename')
    s3 = boto3.client('s3',
                        aws_access_key_id=app.config['ACCESS_KEY_ID'],
                        aws_secret_access_key=app.config['SECRET_ACCESS_KEY'])

    url = s3.generate_presigned_url('get_object', Params = {'Bucket': app.config['S3_BUCKET'], 'Key': filename}, ExpiresIn = 100)
    
    return redirect(url, code=302)

def put_pdf(data):
    filename = data.get('filename')

    if (filename is not None) and ('filedata' in data.keys()):
        fileobj = io.BytesIO(base64.b64decode(data['filedata']))

        s3 = boto3.client('s3',
            aws_access_key_id=app.config['ACCESS_KEY_ID'],
            aws_secret_access_key=app.config['SECRET_ACCESS_KEY']
        )
        try:
            s3.upload_fileobj(
                fileobj,
                app.config['S3_BUCKET'],
                filename,
                ExtraArgs={
                    "ContentType": 'pdf'
                }
            )

        except Exception as e:
            return {'error': str(e)}

        return {'message': 'file posted successfully'}
    
    return {'error': 'missing data'}