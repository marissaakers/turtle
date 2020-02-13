from turtleapi import db
from turtleapi.models.turtlemodels import (LagoonEncounter, Encounter, Turtle, 
Tag, Morphometrics, Sample, Metadata, Net, IncidentalCapture,
TurtleSchema, EncounterSchema, TagSchema, MorphometricsSchema, MetadataSchema,
LagoonEncounterSchema, SampleSchema, NetSchema, IncidentalCaptureSchema)
from datetime import datetime, timedelta
import json
from flask import jsonify
from turtleapi.capture.util import find_turtles_from_tags

def edit_lagoon(data):
    # Declare schema instances
    turtle_schema = TurtleSchema()
    encounter_schema = EncounterSchema()
    tag_schema = TagSchema()
    morphometrics_schema = MorphometricsSchema()
    metadata_schema = MetadataSchema()
    lagoon_encounter_schema = LagoonEncounterSchema()
    sample_schema = SampleSchema()
    # paps_schema = PapsSchema()
    net_schema = NetSchema()
    incidental_capture_schema = IncidentalCaptureSchema()
    # environment_schema = EnvironmentSchema()

    ### Filters

    FILTER_tags = data.get('tags', '')
    FILTER_entered_by = data.get('entered_by', '')
    FILTER_verified_by = data.get('verified_by', '')
    FILTER_investigated_by = data.get('investigated_by', '')

    ### End filters

    turtle_id = data.get('turtle_id', '')
    encounter_id = data.get('encounter_id', '')

    if encounter_id == '':
        print("error: Lagoon edit input is in invalid format")
        return {'error': 'Lagoon edit input is in invalid format'}
    
    edit_encounter = Encounter.query.filter(Encounter.encounter_id == encounter_id).first()

    if edit_encounter is not None:
        # Make output object

        ### Build list of edits
        if FILTER_investigated_by != '':
            edit_encounter.investigated_by = FILTER_investigated_by
        if FILTER_entered_by != '':
            edit_encounter.entered_by = FILTER_entered_by
        if FILTER_verified_by != '':
            edit_encounter.verified_by = FILTER_verified_by
        
        ### commit changes to DB
        db.session.commit()

    return "{}"