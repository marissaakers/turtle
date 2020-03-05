from turtleapi import db
from turtleapi.models.turtlemodels import (TridentEncounter, Encounter, Turtle, Tag,
                                           Morphometrics, Sample, Metadata, Net,
                                           IncidentalCapture)
from datetime import datetime, timedelta
import json
from turtleapi.capture.util import find_turtle_from_tags
from flask import jsonify
import random # we can remove this when we're done and don't do the manual test insertions anymore

def mini_query_trident(data):
    print(test)

def query_trident_metadata(data):
    ### FILTERS
    FILTER_metadata_id = data.get('metadata_id', '')
    FILTER_metadata_date = data.get('metadata_date', '')
    FILTER_metadata_type = "trident"
    ### END FILTERS

    # Build queries
    queries = []

    # queries.append(Metadata.type == "lagoon")
    if (FILTER_metadata_id != ''):
        queries.append(TridentMetadata.metadata_id == FILTER_metadata_id)
    if (FILTER_metadata_date != ''):
        queries.append(TridentMetadata.metadata_date == FILTER_metadata_date)
    if (FILTER_metadata_id == FILTER_metadata_date):
        print("Error: Metadata query missing sufficient data")
        return {'error': 'Metadata query missing sufficient data'}

    # Grab metadata
    result = db.session.query(TridentMetadata).filter(*queries).first()
    if result is None:
        print("Error: Metadata matching criteria not found")
        return {'error': 'Metadata matching criteria not found'}

    result_encounter = result.to_dict(max_nesting=2)
    
    return Response(json.dumps(result_encounter, default = date_handler),mimetype = 'application/json')

def insert_trident_metadata(data):
    metadata = TridentMetadata.new_from_dict(data, error_on_extra_keys=False, drop_extra_keys=True)
    db.session.add(metadata)
    db.session.commit()

    return {'message': 'no errors'}

def insert_trident(data):
    data2 = {}
    data2['encounters'] = data
    data2['tags'] = data2['encounters']['tags']
    del data2['encounters']['tags']
    data2['species'] = data2['encounters']['species']
    del data2['encounters']['species']
    data2['encounters']['morphometrics'] = [data2['encounters']['morphometrics']]

    # handling turtle
    turtle = find_turtle_from_tags(data2['tags'])
    if turtle is not None:
        if data2['encounters']['capture_type'] != "strange recap": # need to make some check for this
            data2['encounters']['capture_type'] = "recap"
        metadata_id = data2['encounters']['metadata_id']
        encounter = TridentEncounter.new_from_dict(data2['encounters'], error_on_extra_keys=False, drop_extra_keys=True)
        encounter.metadata_id = metadata_id
        del data2['encounters']

        compare_tags = db.session.query(Tag).filter(Tag.turtle_id==turtle.turtle_id,Tag.active==True)
        # updating existing tags
        for c in compare_tags:
            flag = False
            i = 0
            for i in range(len(data2['tags'])):
                if c.tag_number == data2['tags'][i]['tag_number']:
                    setattr(c,'tag_scars',data2['tags'][i]['tag_scars'])
                    flag = True
                    del data2['tags'][i]
                    break
                i = i + 1
            if flag == False:
                setattr(c,'active',False)
        # adding new tags
        for t in data2['tags']:
            tag = Tag.new_from_dict(t, error_on_extra_keys=False, drop_extra_keys=True)
            tag.turtle_id = turtle.turtle_id
            db.session.add(tag)
    else:
        if data2['encounters']['capture_type'] != "strange recap": # need to make some check for this
            data2['encounters']['capture_type'] = "recap"
        metadata_id = data2['encounters']['metadata_id']
        encounter = TridentEncounter.new_from_dict(data2['encounters'], error_on_extra_keys=False, drop_extra_keys=True)
        encounter.metadata_id = metadata_id
        turtle = Turtle.new_from_dict(data2, error_on_extra_keys=False, drop_extra_keys=True)

    encounter.turtle = turtle
    db.session.add(encounter)
    db.session.commit()

# ### This is the hard-coded insertion code. It still works if we need to remake db/insert something.
# def insert_trident():
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
#     method = ['dip net','tangle net']

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

#     trident_encounter = TridentEncounter(
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
#         notes="I did not take a lot of notes on this turtle",
#         capture_location="yup somewhere",
#         capture_method=random.choice(method),
#         number_on_carapace=2,
#         disposition_of_specimen="it was angry"
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
#         encounter=trident_encounter,
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
#         flipper_damage='Something should go here',
#         carapace_damage='I am out of ideas'
#     )

#     sample = Sample(
#         encounter=trident_encounter,
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
#         species="Some non-turtle",
#         capture_time=datetime.datetime.now(),
#         measurement = "it is a pretty large creature",
#         notes = "nothing clever to say"
#     )

#     db.session.add(trident_encounter)
#     db.session.commit()
