from turtleapi import db
from turtleapi.models.turtlemodels import (LagoonEncounter, Encounter, Turtle, Tag,
                                           Morphometrics, Sample, Metadata, Net,
                                           IncidentalCapture, TurtleSchema,
                                           EncounterSchema, TagSchema, MorphometricsSchema,
                                           MetadataSchema, LagoonEncounterSchema, SampleSchema,
                                           NetSchema, IncidentalCaptureSchema, FullLagoonQuerySchema)
import datetime
import json
from turtleapi.capture.util import find_turtle_from_tags
from flask import jsonify
import random # we can remove this when we're done and don't do the manual test insertions anymore

def insert_lagoon(data):

    # lagoon_schema = FullLagoonQuerySchema()
    # lagoon = lagoon_schema.load(data, unknown='EXCLUDE')
    # db.session.add(lagoon)
    # db.session.commit()

    # 1) make turtle object
    # 2) db.session.add(turtle)
    # 3) db.session.flush() for turtle
    # 4) make encounter/tags with turtle_id
    # 5) db.session.add(encounter/tags)
    # 6) db.session.flush() for encounter
    # 7) make morphometrics/samples
    # 8) db.session.add(morphometrics/samples)
    # 9) db.session.commit()

    turtle = Turtle.new_from_dict(data, error_on_extra_keys=False, drop_extra_keys=True)
    print(turtle)
    print(turtle.species)
    # db.session.add(turtle)
    # db.session.commit()


#     # Schemas
#     turtle_schema = TurtleSchema()
#     lagoon_encounter_schema = LagoonEncounterSchema()
#     tag_schema = TagSchema()

#     # Insert
#     morphometrics = data.get('morphometrics')
#     # print(morphometrics) # needed? bad list?
#     del data['morphometrics']
#     del data['samples']
#     del data['tags']
#     # print(data)

#    # turtle = turtle_schema.load(data, unknown='EXCLUDE')
#  #   db.session.add(turtle)
#   #  db.session.flush()
#    # db.session.commit()
#     encounter_schema = EncounterSchema()
#     data['turtle_id'] = 9
#     print(data)

#     encounterdata = {
#         'turtle_id': data.get('turtle_id'),
#         'type': data.get('type')
#     }

#     encounter = encounter_schema.load(encounterdata, unknown='EXCLUDE')
#     db.session.add(encounter)
#     tags = tag_schema.load(data, unknown='EXCLUDE')
#     # print("!!TEST!!")
#     # print(tags)
#     db.session.commit()



    # tags = data['tags']
    # encounter = data['encounter']
    # metadata = Metadata.query.filter_by(metadata_id=data['metadata_id']).first()
    # morphometrics = data['morphometrics']
    # samples = encounter['samples']

    # # Attempt to find a turtle from the tags
    # turtle = find_turtle_from_tags(tags)
    
    # tag_list = ()
    # if turtle is None:
    #     turtle = Turtle(
    #         species=data['species']
    #     )
    #     for tag in tags:
    #         new_tag = Tag(
    #             turtle=turtle,
    #             tag_number=tag['tag_number'],
    #             tag_scars=tag['tag_scars'],
    #             active=tag['active'],
    #             tag_type=tag['tag_type']
    #         )
    #         tag_list = tag_list + (new_tag,)
    # else:
    #     for tag in tags:
    #         compare_tag = Tag.query.filter_by(turtle_id=turtle.turtle_id, tag_type=tag['tag_type']).first()
    #         if compare_tag.tag_number != tag['tag_number']:
    #             setattr(compare_tag, 'active', False)
    #             new_tag = Tag(
    #                 turtle=turtle,
    #                 tag_number=tag['tag_number'],
    #                 tag_scars=tag['tag_scars'],
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
    #     metadata=metadata,
    #     encounter_date=encounter['encounter_date'],
    #     encounter_time=encounter['encounter_time'],
    #     investigated_by=encounter['investigated_by'],
    #     entered_by=encounter['entered_by'],
    #     entered_date=encounter['entered_date'],
    #     verified_by=encounter['verified_by'],
    #     verified_date=encounter['verified_date'],
    #     notes=encounter['notes'],
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
    #     flipper_damage=morphometrics['flipper_damage'],
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

    # # db.session.add(tag_list)
    # db.session.add(lagoon_encounter)
    # db.session.commit()

 ###   return something at some point? Maybe previous turtle encounters as well as error variable

# ### This is the hard-coded insertion code. It still works if we need to remake db/insert something.
# def insert_lagoon():
#     # Make a new turtle
#     turtle = Turtle()
#     # See if the turtle exists (we'll change this to find turtles with the given tags)
#     query_result = Turtle.query.filter_by(turtle_id=9).first()
#     # If the turtle is found, we'll use that turtle; otherwise we'll make a new turtle
#     if query_result is not None:
#         turtle = query_result

#     names = ['Matt','Adam','Jade','Marissa','Lucia','Gustavo']
#     tf = [True, False]
#     letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N']
#     timenow = datetime.datetime.now() + datetime.timedelta(days=random.randrange(-2000,2000))

#     turtle = Turtle(
#         species=random.choice(['Loggerhead', 'Leatherback', 'Green Sea Turtle', 'Hawksbill', 'Olive Ridley']),
#     )

#     metadata = Metadata(
#         metadata_date=timenow,
#         metadata_location="My house",
#         metadata_investigators="The whole team",
#         number_of_cc_captured=5 + random.randrange(-3,3),
#         number_of_cm_captured=2 + random.randrange(-2,2),
#         number_of_other_captured=4 + random.randrange(-3,3),
#         water_sample=random.choice(tf),
#         wind_speed=32.6 + round(random.uniform(-3,3), 1),
#         wind_dir="NNW",
#         environment_time=timenow,
#         weather="Partly cloudy",
#         air_temp=33.8,
#         water_temp_surface=29.4 + round(random.uniform(-3,3), 1),
#         water_temp_1_m=41.8 + round(random.uniform(-3,3), 1),
#         water_temp_2_m=39.9 + round(random.uniform(-3,3), 1),
#         water_temp_6_m=48.7 + round(random.uniform(-3,3), 1),
#         water_temp_bottom=51.5 + round(random.uniform(-3,3), 1),
#         salinity_surface=14.8 + round(random.uniform(-3,3), 1),
#         salinity_1_m=10.5 + round(random.uniform(-3,3), 1),
#         salinity_2_m=11.8 + round(random.uniform(-3,3), 1),
#         salinity_6_m=12.8 + round(random.uniform(-3,3), 1),
#         salinity_bottom=19.2 + round(random.uniform(-3,3), 1)
#     )

#     lagoon_encounter = LagoonEncounter(
#         turtle=turtle,
#         metadata=metadata,
#         encounter_date=timenow,
#         encounter_time=timenow,
#         investigated_by=random.choice(names),
#         entered_by=random.choice(names),
#         entered_date=timenow,
#         verified_by=random.choice(names),
#         verified_date=timenow,
#         living_tags=False,
#         other="Other information goes here",
#         leeches=False,
#         leeches_where="",
#         leech_eggs=True,
#         leech_eggs_where="Sadly there are leech eggs on this turtle",
#         paps_present=True,
#         number_of_paps=5,
#         paps_regression="They are not regressing",
#         photos=False,
#         pap_photos=False,
#         notes="I did not take a lot of notes on this turtle"
#     )

#     tag1 = Tag(
#         turtle=turtle,
#         tag_number=random.choice(letters) + random.choice(letters) + str(random.randint(1000,9999)),
#         tag_scars=False,
#         active=True,
#         tag_type="LF"
#     )

#     tag2 = Tag(
#         turtle=turtle,
#         tag_number=random.choice(letters) + random.choice(letters) + str(random.randint(1000,9999)),
#         tag_scars=False,
#         active=True,
#         tag_type="RF"
#     )

#     tag3 = Tag(
#         turtle=turtle,
#         tag_number=random.choice(letters) + random.choice(letters) + str(random.randint(1000,9999)),
#         tag_scars=False,
#         active=True,
#         tag_type="PIT"
#     )

#     tags = (tag1, tag2, tag3)

#     morphometrics = Morphometrics(
#         turtle=turtle,
#         encounter=lagoon_encounter,
#         curved_length=14.0 + round(random.uniform(-3,3), 1),
#         straight_length=23.7 + round(random.uniform(-3,3), 1),
#         minimum_length=12.5 + round(random.uniform(-3,3), 1),
#         plastron_length=50.2 + round(random.uniform(-3,3), 1),
#         weight=132 + round(random.uniform(-3,3), 1),
#         curved_width=32.0 + round(random.uniform(-3,3), 1),
#         straight_width=14.5 + round(random.uniform(-3,3), 1),
#         tail_length_pl_vent=32.0 + round(random.uniform(-3,3), 1),
#         tail_length_pl_tip=31.9 + round(random.uniform(-3,3), 1),
#         head_width=7.1 + round(random.uniform(-3,3), 1),
#         body_depth=14.1 + round(random.uniform(-3,3), 1),
#         flipper_carapace='Something should go here',
#         carapace_damage='I am out of ideas'
#     )

#     sample = Sample(
#         encounter=lagoon_encounter,
#         skin_1=True,
#         skin_1_for="NO IDEA",
#         skin_2=True,
#         skin_2_for="Skin text",
#         blood=False,
#         blood_for="",
#         scute=False,
#         scute_for="",
#         other=False,
#         other_for=""
#     )

#     net = Net(
#         metadata=metadata,
#         net_number=3,
#         net_deploy_start_time=timenow,
#         net_deploy_end_time=timenow,
#         net_retrieval_start_time=timenow,
#         net_retrieval_end_time=timenow
#     )

#     incidental_capture = IncidentalCapture(
#         metadata=metadata,
#         species="Some turtle",
#         capture_time=datetime.datetime.now(),
#         measurement = "it is a pretty large turtle",
#         notes = "nothing clever to say"
#     )

#     db.session.add(lagoon_encounter)
#     db.session.commit()
