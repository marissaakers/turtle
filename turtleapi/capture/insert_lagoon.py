from turtleapi import db
from turtleapi.models.turtlemodels import (LagoonEncounter, Encounter, Turtle, Tag,
                                           Morphometrics, Sample, Metadata, Net,
                                           IncidentalCapture, TurtleSchema,
                                           EncounterSchema, TagSchema, MorphometricsSchema,
                                           MetadataSchema, LagoonEncounterSchema, SampleSchema,
                                           NetSchema, IncidentalCaptureSchema)
import datetime
import json
from turtleapi.capture.util import find_turtle_from_tags, insert_new_tags
from flask import jsonify
import random # we can remove this when we're done and don't do the manual test insertions anymore
from sqlalchemy import func

def insert_lagoon(data):

    # 1) make turtle object
    # 2) db.session.add(turtle)
    # 3) db.session.flush() for turtle
    # 4) make encounter/tags with turtle_id
    # 5) db.session.add(encounter/tags)
    # 6) db.session.flush() for encounter
    # 7) make morphometrics/samples
    # 8) db.session.add(morphometrics/samples)
    # 9) db.session.commit()

    # Schemas
    turtle_schema = TurtleSchema()
    lagoon_encounter_schema = LagoonEncounterSchema()
    tag_schema = TagSchema()
    morphometrics_schema = MorphometricsSchema()
    sample_schema = SampleSchema()
    tag_schema = TagSchema()

    # Insert
    data_morphometrics = data.get('morphometrics')
    data_tags = data.get('tags')
    data_samples = data.get('samples')
    del data['samples']
    del data['tags']
    del data['morphometrics']

    turtle = turtle_schema.load(data, unknown='EXCLUDE')
    db.session.add(turtle)
    db.session.flush()
    
    stupid_next_id = db.session.query(func.max(Encounter.encounter_id)).first()
    # Handle stupid "first insert" edge case
    if stupid_next_id[0] is None:
        stupid_next_id = 0
    else:
        stupid_next_id = stupid_next_id[0]
    data['encounter_id'] = stupid_next_id + 1
    lagoon_encounter = lagoon_encounter_schema.load(data, unknown='EXCLUDE')
    lagoon_encounter.turtle=turtle
    db.session.add(lagoon_encounter)
    db.session.flush()

    morphometrics = morphometrics_schema.load(data_morphometrics, unknown='EXCLUDE')
    morphometrics.encounter = lagoon_encounter
    db.session.add(morphometrics)
    print(morphometrics_schema.dump(morphometrics))
    db.session.flush()

    if data_samples != {}:
        samples = sample_schema.load(data_samples, unknown='EXCLUDE')
        db.session.add(samples)

    db.session.commit()

    insert_new_tags(data_tags)
