from turtleapi import db
from turtleapi.models.turtlemodels import (LagoonEncounter, Encounter, Turtle, 
Tag, Morphometrics, Sample, Paps, Metadata, Net, IncidentalCapture, Environment)
import datetime
import json

def insert_lagoon():
    # Make a new turtle
    turtle = Turtle()
    # See if the turtle exists (we'll change this to find turtles with the given tags)
    query_result = Turtle.query.filter_by(turtle_id=9).first()
    # If the turtle is found, we'll use that turtle; otherwise we'll make a new turtle
    if query_result is not None:
        turtle = query_result

    metadata = Metadata(
        metadata_date=datetime.datetime.now(),
        metadata_location="My house",
        metadata_investigators="The whole team",
        number_of_cc_captured=5,
        number_of_cm_captured=2,
        number_of_other_captured=4
    )

    encounter = Encounter(
        turtle=turtle,
        metadata=metadata,
        encounter_date=datetime.datetime.now(),
        encounter_time=datetime.datetime.now(),
        species="Unknown species",
        investigated_by="Adam",
        entered_by="Matt",
        entered_date=datetime.datetime.now(),
        verified_by="Jade",
        verified_date=datetime.datetime.now()
    )

    lagoon_encounter = LagoonEncounter(
        encounter=encounter,
        living_tags=False,
        other="Other information goes here",
        leeches=False,
        leeches_where="",
        leech_eggs=True,
        leech_eggs_where="Sadly there are leech eggs on this turtle"
    )

    db.session.add(lagoon_encounter)
    db.session.commit()

    lagoon_encounters = LagoonEncounter.query.all()
    return lagoon_encounters

