from turtleapi import db, ma
from flask import jsonify

class Turtle(db.Model):
	turtle_id = db.Column(db.Integer, primary_key=True)
	clutches = db.relationship('Clutch', backref='turtle', lazy=True)
	morphometrics = db.relationship('Morphometrics', backref='turtle', lazy=True)

class Clutch(db.Model):
	clutch_id = db.Column(db.Integer, primary_key=True)
	turtle_id = db.Column(db.Integer, db.ForeignKey('turtle.turtle_id'), nullable=False)
	hatchlings = db.relationship('Hatchlings', backref='clutch', lazy=True)
	eggs = db.relationship('Eggs', backref='clutch', lazy=True)
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

class Hatchlings(db.Model):
	hatchlings_id = db.Column(db.Integer, primary_key=True)
	clutch_id = db.Column(db.Integer, db.ForeignKey('clutch.clutch_id'), nullable=False)
	hatched = db.Column(db.Integer)
	live_hatchlings = db.Column(db.Integer)
	dead_hatchlings = db.Column(db.Integer)
	hatchlings_emerged = db.Column(db.Integer)
	pipped_live = db.Column(db.Integer)
	pipped_dead = db.Column(db.Integer)

class Eggs(db.Model):
	eggs_id = db.Column(db.Integer, primary_key=True)
	clutch_id = db.Column(db.Integer, db.ForeignKey('clutch.clutch_id'), nullable=False)
	eggs_eggs = db.Column(db.Integer)
	eggs_undeveloped = db.Column(db.Integer)
	eggs_sampled_for_sac = db.Column(db.Integer)
	eggs_1_4_embryo = db.Column(db.Integer)
	eggs_2_4_embryo = db.Column(db.Integer)
	eggs_3_4_embryo = db.Column(db.Integer)
	eggs_4_4_embryo = db.Column(db.Integer)
	eggs_damaged_racoons = db.Column(db.Integer)
	eggs_damaged_ghost_crabs = db.Column(db.Integer)
	egg_damaged_plant_roots = db.Column(db.Integer)
	eggs_damaged_another_turtle = db.Column(db.Integer)
	eggs_damaged_bobcat = db.Column(db.Integer)
	eggs_damaged_other = db.Column(db.Integer)
	eggs_damaged_plant_details = db.Column(db.Text)
	eggs_broken = db.Column(db.Integer)
	eggs_washout = db.Column(db.Integer)
	eggs_other = db.Column(db.Integer)
	eggs_other_details = db.Column(db.Text)
	eggs_yolkless_hydrated = db.Column(db.Integer)
	eggs_yolkless_dehydrated = db.Column(db.Integer)
	clutch_size = db.Column(db.Integer)
	substrate = db.Column(db.String(50))
	notes = db.Column(db.Text)

class Morphometrics(db.Column):
	morphometrics_id = db.Column(db.Integer, primary_key=True)
	turtle_id = db.Column(db.Integer, db.ForeignKey('turtle.turtle_id'), nullable=False)
	curved_length = db.Column(db.Float(5))
	straight_length = db.Column(db.Float(5))
	minimum_length = db.Column(db.Float(5))
	plastron_length = db.Column(db.Float(5))
	weight = db.Column(db.Float(5))
	curved_width = db.Column(db.Float(5))
	straight_width = db.Column(db.Float(5))
	tail_length_pl_vent = db.Column(db.Float(5))
	tail_length_pl_tip = db.Column(db.Float(5))
	head_width = db.Column(db.Float(5))
	body_depth = db.Column(db.Float(5))
	flipper_carapace = db.Column(db.Text)
	carapace_damage = db.Column(db.Text)

class TurtleSchema(ma.ModelSchema):
	class Meta:
		model = Turtle

class ClutchSchema(ma.ModelSchema):
	class Meta:
		model = Clutch

class HatchlingsSchema(ma.ModelSchema):
	class Meta:
		model = Hatchlings

class EggsSchema(ma.ModelSchema):
	class Meta:
		model = Eggs

class MorphometricsSchema(ma.ModelSchema):
	class Meta:
		model = Morphometrics