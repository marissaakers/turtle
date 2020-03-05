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