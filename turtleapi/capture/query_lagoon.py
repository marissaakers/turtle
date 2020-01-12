from turtleapi import db
from turtleapi.models.turtlemodels import (LagoonEncounter, Encounter, Turtle, 
Tag, Morphometrics, Sample, Paps, Metadata, Net, IncidentalCapture, Environment,
TurtleSchema, EncounterSchema, TagSchema, MorphometricsSchema, MetadataSchema,
LagoonEncounterSchema, SampleSchema, PapsSchema, NetSchema, IncidentalCaptureSchema, 
EnvironmentSchema)
import datetime
import json
from flask import jsonify

def query_lagoon():
    # Declare schema instances
    turtle_schema = TurtleSchema()
    encounter_schema = EncounterSchema()
    tag_schema = TagSchema()
    morphometrics_schema = MorphometricsSchema()
    metadata_schema = MetadataSchema()
    lagoon_encounter_schema = LagoonEncounterSchema()
    sample_schema = SampleSchema()
    paps_schema = PapsSchema()
    net_schema = NetSchema()
    incidental_capture_schema = IncidentalCaptureSchema()
    environment_schema = EnvironmentSchema()

    # Grab turtle
    turtle_result = Turtle.query.first()

    # Make output object
    output = turtle_schema.dump(turtle_result)

    # Grab encounters
    encounter_id = output['encounters'][0]
    encounter_result = Encounter.query.filter_by(encounter_id=encounter_id).first()
    output['encounters'] = encounter_schema.dump(encounter_result)

    # Grab tags
    turtle_id = output['turtle_id']
    tag_result = Tag.query.filter_by(turtle_id=turtle_id).all()
    output['tags'] = tag_schema.dump(tag_result, many=True)

    # Grab morphometrics
    morphometrics_id = output['morphometrics'][0]
    morphometrics_result = Morphometrics.query.filter_by(morphometrics_id=morphometrics_id).first()
    output['morphometrics'] = morphometrics_schema.dump(morphometrics_result)

    # Grab metadata
    metadata_id = output['encounters']['metadata']
    metadata_result = Metadata.query.filter_by(metadata_id=metadata_id).first()
    output['metadata'] = metadata_schema.dump(metadata_result)
    del output['encounters']['metadata']

    # Grab lagoon_encounter
    lagoon_encounter_result = LagoonEncounter.query.filter_by(encounter_id=encounter_id).first()
    output['encounters']['lagoon_encounter'] = lagoon_encounter_schema.dump(lagoon_encounter_result)

    # Grab paps
    paps_result = Paps.query.filter_by(encounter_id=encounter_id).first()
    output['encounters']['paps'] = paps_schema.dump(paps_result)

    # Grab samples
    samples_result = Sample.query.filter_by(encounter_id=encounter_id).all()
    output['encounters']['samples'] = sample_schema.dump(samples_result, many=True)

    # Grab nets
    nets_result = Net.query.filter_by(metadata_id=metadata_id).all()
    output['metadata']['nets'] = net_schema.dump(nets_result, many=True)

    # Grab incidental captures
    incidental_captures_result = IncidentalCapture.query.filter_by(metadata_id=metadata_id).all()
    output['metadata']['incidental_captures'] = incidental_capture_schema.dump(incidental_captures_result, many=True)

    # Grab environment
    environment_result = Environment.query.filter_by(metadata_id=metadata_id).first()
    output['metadata']['environment'] = environment_schema.dump(environment_result)

    return output