from turtleapi import db
from turtleapi.models.turtlemodels import (LagoonEncounter, Encounter, Turtle, 
Tag, Morphometrics, Sample, Paps, Metadata, Net, IncidentalCapture, Environment)
import datetime
import json

def insert_lagoon():
    turtle = Turtle(turtle_id=7)
    db.session.add(turtle)
    db.session.commit()

    turtles = Turtle.query.all()
    return turtles

	# turtle_id = db.Column(db.Integer, primary_key=True)
	# tags = db.relationship('Tag', backref='turtle', lazy=True)
	# clutches = db.relationship('Clutch', backref='turtle', lazy=True)
	# morphometrics = db.relationship('Morphometrics', backref='turtle', lazy=True)
	# encounters = db.relationship('Encounter', backref='turtle', lazy=True)	

    # lagoon_encounter = LagoonEncounter(
    #     0,
    #     False,
    #     "Other information goes here",
    #     False,
    #     "",
    #     True,
    #     "Sadly there are leech eggs on this turtle"
    # )

    # db.session.add(lagoon_encounter)
    # db.session.add(encounter)
    # db.commit()

    # encounter = Encounter(
    #     0,
    #     0,
    #     datetime.datetime.now(),
    #     datetime.datetime.now(),
    #     "Unknown species",
    #     "Adam",
    #     "Matt",
    #     datetime.datetime.now(),
    #     "Jade",
    #     datetime.datetime.now()
    # )

    # lagoon_encounter = LagoonEncounter(
    #     0,
    #     False,
    #     "Other information goes here",
    #     False,
    #     "",
    #     True,
    #     "Sadly there are leech eggs on this turtle"
    # )
        

