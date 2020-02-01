from turtleapi import db
from turtleapi.models.turtlemodels import (LagoonEncounter, Encounter, Turtle, 
Tag, Morphometrics, Sample, Paps, Metadata, Net, IncidentalCapture, Environment,
TurtleSchema, EncounterSchema, TagSchema, MorphometricsSchema, MetadataSchema,
LagoonEncounterSchema, SampleSchema, PapsSchema, NetSchema, IncidentalCaptureSchema, 
EnvironmentSchema)
from datetime import datetime, timedelta
import json
from flask import jsonify
from turtleapi.capture.util import find_turtles_from_tags

def query_lagoon(data):
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

    input_tags = data.get('tags', '')
    print(input_tags)

    #FILTER_TURTLE_ID = data.get

    FILTER_SPECIES = data.get('species', '') # Only match this species

    string_date_start = data.get('start_date', '') # Match between FILTER_DATE_START and FILTER_DATE_END
    string_date_end = data.get('end_date', '')
    if string_date_start != '':
        FILTER_DATE_START = datetime.strptime(string_date_start, '%m/%d/%Y') # .date()
        FILTER_DATE_END = datetime.strptime(string_date_end, '%m/%d/%Y')

    queries = []

    # if input_tags != '':
    #     turtles = find_turtles_from_tags(input_tags)
    #     print(turtles)

    # Grab turtles
    turtle_result = Turtle.query.filter(*queries).all()

    # Make output object
    output = turtle_schema.dump(turtle_result, many=True)
    t_counter = -1

    for turtle in turtle_result:
        t_counter += 1

        turtle_id = turtle.turtle_id
        t_output = output[t_counter]
        t_output['turtle_id'] = turtle_id
        del t_output['morphometrics']

        # Grab tags
        tag_result = Tag.query.filter_by(turtle_id=turtle_id).all()
        t_output['tags'] = tag_schema.dump(tag_result, many=True)

        # Build list of queries
        queries.clear()
        queries.append(Encounter.turtle_id == turtle_id)

        if FILTER_SPECIES != '':
            queries.append(Encounter.species == FILTER_SPECIES)
        if string_date_start != '':
            queries.append(Encounter.encounter_date >= FILTER_DATE_START)
            queries.append(Encounter.encounter_date <= FILTER_DATE_END)
        
        # Grab encounters, filter by anything appended above
        encounter_result = Encounter.query.filter(*queries).all()

        if not encounter_result:
            del output[t_counter]
            t_counter -= 1
            continue
        t_output['encounters'] = lagoon_encounter_schema.dump(encounter_result, many=True)
        e_counter = -1

        for encounter in encounter_result:
            e_counter += 1

            encounter_id = encounter.encounter_id
            e_output = t_output['encounters'][e_counter]

            # Grab morphometrics
            morphometrics_result = Morphometrics.query.filter_by(encounter_id=encounter_id).first() # Only one morph per encounter ya?
            e_output['morphometrics'] = morphometrics_schema.dump(morphometrics_result)

            # Grab metadata
            metadata_id = encounter.metadata_id
            metadata_result = Metadata.query.filter_by(metadata_id=metadata_id).first()
            e_output['metadata'] = metadata_schema.dump(metadata_result)
            del e_output['metadata']['encounters']

            # Grab paps
            paps_result = Paps.query.filter_by(encounter_id=encounter_id).first()
            e_output['paps'] = paps_schema.dump(paps_result)

            # Grab samples
            samples_result = Sample.query.filter_by(encounter_id=encounter_id).all()
            e_output['samples'] = sample_schema.dump(samples_result, many=True)

            # Grab nets
            nets_result = Net.query.filter_by(metadata_id=metadata_id).all()
            e_output['metadata']['nets'] = net_schema.dump(nets_result, many=True)

            # Grab incidental captures
            incidental_captures_result = IncidentalCapture.query.filter_by(metadata_id=metadata_id).all()
            e_output['metadata']['incidental_captures'] = incidental_capture_schema.dump(incidental_captures_result, many=True)

            # Grab environment
            environment_result = Environment.query.filter_by(metadata_id=metadata_id).first()
            e_output['metadata']['environment'] = environment_schema.dump(environment_result)

    return output