from turtleapi import db
from turtleapi.models.turtlemodels import (LagoonEncounter, Encounter, Turtle, Tag,
                                           Morphometrics, Sample, Metadata, Net,
                                           IncidentalCapture, TurtleSchema,
                                           EncounterSchema, TagSchema, MorphometricsSchema,
                                           MetadataSchema, LagoonEncounterSchema, SampleSchema,
                                           NetSchema, IncidentalCaptureSchema)
import datetime
import json
from turtleapi.capture.util import find_turtle_from_tags
from flask import jsonify

# def insert_lagoon(data):
    # tags = data['tags']
    # encounter = data['encounter']
    # metadata = data['metadata']
    # morphometrics = data['morphometrics']
    # samples = encounter['samples']
    # # paps = encounter['paps']
    # nets = metadata['nets']
    # # environment = metadata['environment']
    # incidental_captures = metadata['incidental_captures']

    # # Attempt to find a turtle from the tags
    # turtle = find_turtle_from_tags(tags)
    # tag_list = ()
    # if turtle is None:
    #     turtle = Turtle()
    #     for tag in tags:
    #         new_tag = Tag(
    #             turtle=turtle,
    #             tag_number=tag['tag_number'],
    #             location=tag['location'],
    #             active=tag['active'],
    #             tag_type=tag['tag_type']
    #         )
    #         tag_list = tag_list + (new_tag,)
    # else:
    #     for tag in tags:
    #         compare_tag = Tag.query.filter_by(location=tag['location'], active=True)
    #         if compare_tag.tag_number != tag['tag_number']:
    #             compare_tag.active = False
    #             db.session.commit() # Is this necessary to update tag -> inactive?
    #             new_tag = Tag(
    #                 turtle=turtle,
    #                 tag_number=tag['tag_number'],
    #                 location=tag['location'],
    #                 active=tag['active'],
    #                 tag_type=tag['tag_type']
    #             )
    #             tag_list = tag_list + (new_tag,)

    # metadata_item = Metadata(
    #     metadata_date=metadata['metadata_date'],
    #     metadata_location=metadata['metadata_location'],
    #     metadata_investigators=metadata['metadata_investigators'],
    #     number_of_cc_captured=metadata['number_of_cc_captured'],
    #     number_of_cm_captured=metadata['number_of_cm_captured'],
    #     number_of_other_captured=metadata['number_of_other_captured'],
    #     water_sample=metadata['water_sample'],
    #     wind_speed=metadata['wind_speed'],
    #     wind_dir=metadata['wind_dir'],
    #     environment_time=metadata['environment_time'],
    #     weather=metadata['weather'],
    #     air_temp=metadata['air_temp'],
    #     water_temp_surface=metadata['water_temp_surface'],
    #     water_temp_1_m=metadata['water_temp_1_m'],
    #     water_temp_2_m=metadata['water_temp_2_m'],
    #     water_temp_6_m=metadata['water_temp_6_m'],
    #     water_temp_bottom=metadata['water_temp_bottom'],
    #     salinity_surface=metadata['salinity_surface'],
    #     salinity_1_m=metadata['salinity_1_m'],
    #     salinity_2_m=metadata['salinity_2_m'],
    #     salinity_6_m=metadata['salinity_6_m'],
    #     salinity_bottom=metadata['salinity_bottom']
    # )

    # lagoon_encounter = LagoonEncounter(
    #     turtle=turtle,
    #     metadata=metadata_item,
    #     encounter_date=encounter['encounter_date'],
    #     encounter_time=encounter['encounter_time'],
    #     species=encounter['species'],
    #     investigated_by=encounter['investigated_by'],
    #     entered_by=encounter['entered_by'],
    #     entered_date=encounter['entered_date'],
    #     verified_by=encounter['verified_by'],
    #     verified_date=encounter['verified_date'],
    #     living_tags=encounter['living_tags'],
    #     other=encounter['other'],
    #     leeches=encounter['leeches'],
    #     leeches_where=encounter['leeches_where'],
    #     leech_eggs=encounter['leech_eggs'],
    #     leech_eggs_where=encounter['leech_eggs_where'],
    #     paps_present=encounter['paps_present'],
    #     number_of_paps=encounter['number_of_paps'],
    #     paps_regression=encounter['paps_regression'],
    #     photos=encounter['photos'],
    #     pap_photos=encounter['pap_photos']
    # )

    # morphometrics_item = Morphometrics(
    #     turtle=turtle,
    #     encounter=lagoon_encounter,
    #     curved_length=morphometrics['curved_length'],
    #     straight_length=morphometrics['straight_length'],
    #     minimum_length=morphometrics['minimum_length'],
    #     plastron_length=morphometrics['plastron_length'],
    #     weight=morphometrics['weight'],
    #     curved_width=morphometrics['curved_width'],
    #     straight_width=morphometrics['straight_width'],
    #     tail_length_pl_vent=morphometrics['tail_length_pl_vent'],
    #     tail_length_pl_tip=morphometrics['tail_length_pl_tip'],
    #     head_width=morphometrics['head_width'],
    #     body_depth=morphometrics['body_depth'],
    #     flipper_carapace=morphometrics['flipper_carapace'],
    #     carapace_damage=morphometrics['carapace_damage']
    # )

    # sample_list = ()
    # for sample in samples:
    #     new_sample = Sample(
    #         encounter=lagoon_encounter,
    #         skin_1=sample['skin_1'],
    #         skin_1_for=sample['skin_1_for'],
    #         skin_2=sample['skin_2'],
    #         skin_2_for=sample['skin_2_for'],
    #         blood=sample['blood'],
    #         blood_for=sample['blood_for'],
    #         scute=sample['scute'],
    #         scute_for=sample['scute_for'],
    #         other=sample['other'],
    #         other_for=sample['other_for']
    #     )
    #     sample_list = sample_list + (new_sample,)

    # net_list = ()
    # for net in nets:
    #     new_net = Net(
    #         metadata=metadata_item,
    #         net_number=net['net_number'],
    #         net_deploy_start_time=net['net_deploy_start_time'],
    #         net_deploy_end_time=net['net_deploy_end_time'],
    #         net_retrieval_start_time=net['net_retrieval_start_time'],
    #         net_retrieval_end_time=net['net_retrieval_end_time']
    #     )
    #     net_list = net_list + (new_net,)

    # incidental_capture_list = ()
    # for incidental_capture in incidental_captures:
    #     new_incidental_capture = IncidentalCapture(
    #         metadata=metadata_item,
    #         species=incidental_capture['species'],
    #         capture_time=incidental_capture['capture_time'],
    #         measurement=incidental_capture['measurement'],
    #         notes=incidental_capture['notes']
    #     )
    # incidental_capture_list = incidental_capture_list + (new_incidental_capture,)

    # db.session.add(lagoon_encounter)
    # db.session.add(environment_item)
    # db.session.commit()

    # return something at some point? Maybe previous turtle encounters as well as error variable

### This is the hard-coded insertion code. It still works if we need to remake db/insert something.
def insert_lagoon():
    # Make a new turtle
    turtle = Turtle()
    # See if the turtle exists (we'll change this to find turtles with the given tags)
    query_result = Turtle.query.filter_by(turtle_id=9).first()
    # If the turtle is found, we'll use that turtle; otherwise we'll make a new turtle
    if query_result is not None:
        turtle = query_result
    
    turtle = Turtle(
        species="Loggerhead",
    )

    metadata = Metadata(
        metadata_date=datetime.datetime.now(),
        metadata_location="My house",
        metadata_investigators="The whole team",
        number_of_cc_captured=5,
        number_of_cm_captured=2,
        number_of_other_captured=4,
        water_sample=False,
        wind_speed=32.6,
        wind_dir="NNW",
        environment_time=datetime.datetime.now(),
        weather="Partly cloudy",
        air_temp=33.8,
        water_temp_surface=29.4,
        water_temp_1_m=41.8,
        water_temp_2_m=39.9,
        water_temp_6_m=48.7,
        water_temp_bottom=51.5,
        salinity_surface=14.8,
        salinity_1_m=10.5,
        salinity_2_m=11.8,
        salinity_6_m=12.8,
        salinity_bottom=19.2
    )

    lagoon_encounter = LagoonEncounter(
        turtle=turtle,
        metadata=metadata,
        encounter_date=datetime.datetime.now(),
        encounter_time=datetime.datetime.now(),
        investigated_by="Matt",
        entered_by="Jade",
        entered_date=datetime.datetime.now(),
        verified_by="Adam",
        verified_date=datetime.datetime.now(),
        living_tags=False,
        other="Other information goes here",
        leeches=False,
        leeches_where="",
        leech_eggs=True,
        leech_eggs_where="Sadly there are leech eggs on this turtle",
        paps_present=True,
        number_of_paps=5,
        paps_regression="They are not regressing",
        photos=False,
        pap_photos=False
    )

    tag1 = Tag(
        turtle=turtle,
        tag_number="BB123456",
        location="LF",
        active=True,
        tag_type="I don't know what this is"
    )

    tag2 = Tag(
        turtle=turtle,
        tag_number="CD765432",
        location="RF",
        active=True,
        tag_type="I don't know what this is"
    )

    tag3 = Tag(
        turtle=turtle,
        tag_number="CC999999",
        location="RR",
        active=True,
        tag_type="I don't know what this is"
    )

    tags = (tag1, tag2, tag3)

    morphometrics = Morphometrics(
        turtle=turtle,
        encounter=lagoon_encounter,
        curved_length=14.0,
        straight_length=23.7,
        minimum_length=12.5,
        plastron_length=50.2,
        weight=132,
        curved_width=32.0,
        straight_width=14.5,
        tail_length_pl_vent=32.0,
        tail_length_pl_tip=31.9,
        head_width=7.1,
        body_depth=14.1,
        flipper_carapace='Something should go here',
        carapace_damage='I am out of ideas'
    )

    sample = Sample(
        encounter=lagoon_encounter,
        skin_1=True,
        skin_1_for="NO IDEA",
        skin_2=True,
        skin_2_for="Skin text",
        blood=False,
        blood_for="",
        scute=False,
        scute_for="",
        other=False,
        other_for=""
    )

    net = Net(
        metadata=metadata,
        net_number=3,
        net_deploy_start_time=datetime.datetime.now(),
        net_deploy_end_time=datetime.datetime.now(),
        net_retrieval_start_time=datetime.datetime.now(),
        net_retrieval_end_time=datetime.datetime.now()
    )

    incidental_capture = IncidentalCapture(
        metadata=metadata,
        species="Some turtle",
        capture_time=datetime.datetime.now(),
        measurement = "it is a pretty large turtle",
        notes = "nothing clever to say"
    )

    db.session.add(lagoon_encounter)
    db.session.commit()
