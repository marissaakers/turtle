from turtleapi import db
from turtleapi.models.turtlemodels import (LagoonEncounter, Encounter, Turtle, 
Tag, Morphometrics, Sample, Paps, Metadata, Net, IncidentalCapture, Environment,
TurtleSchema, EncounterSchema, TagSchema, MorphometricsSchema, MetadataSchema,
LagoonEncounterSchema, SampleSchema, PapsSchema, NetSchema, IncidentalCaptureSchema, 
EnvironmentSchema)
import datetime
import json
from flask import jsonify

def insert_lagoon(data):
    metadata = data['metadata']
    return metadata

# def insert_lagoon():
    # # Make a new turtle
    # turtle = Turtle()
    # # See if the turtle exists (we'll change this to find turtles with the given tags)
    # query_result = Turtle.query.filter_by(turtle_id=9).first()
    # # If the turtle is found, we'll use that turtle; otherwise we'll make a new turtle
    # if query_result is not None:
    #     turtle = query_result

    # metadata = Metadata(
    #     metadata_date=datetime.datetime.now(),
    #     metadata_location="My house",
    #     metadata_investigators="The whole team",
    #     number_of_cc_captured=5,
    #     number_of_cm_captured=2,
    #     number_of_other_captured=4
    # )

    # encounter = Encounter(
    #     turtle=turtle,
    #     metadata=metadata,
    #     encounter_date=datetime.datetime.now(),
    #     encounter_time=datetime.datetime.now(),
    #     species="Unknown species",
    #     investigated_by="Adam",
    #     entered_by="Matt",
    #     entered_date=datetime.datetime.now(),
    #     verified_by="Jade",
    #     verified_date=datetime.datetime.now()
    # )

    # lagoon_encounter = LagoonEncounter(
    #     encounter=encounter,
    #     living_tags=False,
    #     other="Other information goes here",
    #     leeches=False,
    #     leeches_where="",
    #     leech_eggs=True,
    #     leech_eggs_where="Sadly there are leech eggs on this turtle"
    # )

    # tag1 = Tag(
    #     turtle=turtle,
    #     tag_number="AA123456",
    #     location="LF",
    #     active=True,
    #     tag_type="I don't know what this is"
    # )

    # tag2 = Tag(
    #     turtle=turtle,
    #     tag_number="BB765432",
    #     location="RF",
    #     active=True,
    #     tag_type="I don't know what this is"
    # )

    # tag3 = Tag(
    #     turtle=turtle,
    #     tag_number="CC989898",
    #     location="RR",
    #     active=True,
    #     tag_type="I don't know what this is"
    # )

    # tags = (tag1, tag2, tag3)

    # morphometrics = Morphometrics(
    #     turtle=turtle,
    #     encounter=encounter,
    #     curved_length=14.0,
    #     straight_length=23.7,
    #     minimum_length=12.5,
    #     plastron_length=50.2,
    #     weight=132,
    #     curved_width=32.0,
    #     straight_width=14.5,
    #     tail_length_pl_vent=32.0,
    #     tail_length_pl_tip=31.9,
    #     head_width=7.1,
    #     body_depth=14.1,
    #     flipper_carapace='Something should go here',
    #     carapace_damage='I am out of ideas'
    # )

    # sample = Sample(
    #     encounter=encounter,
    #     skin_1=True,
    #     skin_1_for="NO IDEA",
    #     skin_2=True,
    #     skin_2_for="Skin text",
    #     blood=False,
    #     blood_for="",
    #     scute=False,
    #     scute_for="",
    #     other=False,
    #     other_for=""
    # )

    # paps = Paps(
    #     encounter=encounter,
    #     paps_present=True,
    #     number_of_paps=5,
    #     paps_regression="They are not regressing",
    #     photos=False,
    #     pap_photos=False      
    # )

    # net = Net(
    #     metadata=metadata,
    #     net_number=3,
    #     net_deploy_start_time=datetime.datetime.now(),
    #     net_deploy_end_time=datetime.datetime.now(),
    #     net_retrieval_start_time=datetime.datetime.now(),
    #     net_retrieval_end_time=datetime.datetime.now()
    # )

    # environment = Environment(
    #     metadata_=metadata,
    #     water_sample=False,
    #     wind_speed=32.6,
    #     wind_dir="NNW",
    #     environment_time=datetime.datetime.now(),
    #     weather="Partly cloudy",
    #     air_temp=33.8,
    #     water_temp_surface=29.4,
    #     water_temp_1_m=41.8,
    #     water_temp_2_m=39.9,
    #     water_temp_6_m=48.7,
    #     water_temp_bottom=51.5,
    #     salinity_surface=14.8,
    #     salinity_1_m=10.5,
    #     salinity_2_m=11.8,
    #     salinity_6_m=12.8,
    #     salinity_bottom=19.2
    # )

    # incidental_capture = IncidentalCapture(
    #     metadata=metadata,
    #     species="Some turtle",
    #     capture_time=datetime.datetime.now(),
    #     measurement = "it is a pretty large turtle",
    #     notes = "nothing clever to say"
    # )

    # db.session.add(lagoon_encounter)
    # db.session.add(environment)
    # db.session.commit()