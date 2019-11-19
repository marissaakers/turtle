from turtleapi import db, ma
from flask import jsonify

class Clutch(db.Model):
	clutch_id = db.Column(db.Integer, primary_key=True)
	## turtle_id here ##
	clutch_deposited = db.Column(db.Boolean)
	sand_type = db.Column(db.String(50))
	placement = db.Column(db.String(50))
	emergence_date = db.Column(db.Date)
	inventory_date = db.Column(db.Date)
	hidden_stake_in_place = db.Column(db.Boolean)
	obvious_stake_in_place = db.Column(db.Boolean)
	emergence = db.Column(db.Boolean)
	s_can_in_place = db.Column(db.Boolean)
	n_can_in_place = db.Column(db.Boolean)
	predated = db.Column(db.Boolean)
	post_hatch = db.Column(db.Boolean)
	washed_over = db.Column(db.Boolean)
	inundated = db.Column(db.Boolean)
	washed_out = db.Column(db.String(20))
	washed_out_post_hatch = db.Column(db.Boolean)
	poached = db.Column(db.Boolean)
	inventoried_by = db.Column(db.String(40))
	entered_by = db.Column(db.String(40))
	entered_date = db.Column(db.Date)
	verified_by = db.Column(db.String(40))
	verified_date = db.Column(db.Date)

class ClutchSchema(ma.ModelSchema):
	class Meta:
		model = Clutch