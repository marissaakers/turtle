from turtleapi import db, ma
from flask import jsonify

class Turtle(db.Model):
	turtle_id = db.Column(db.Integer, primary_key=True)
	tags = db.relationship('Tag', backref='turtle')
	clutches = db.relationship('Clutch', backref='turtle')
	morphometrics = db.relationship('Morphometrics', backref='turtle')
	encounters = db.relationship('Encounter', backref='turtle', lazy='dynamic')	

class Tag(db.Model):
	tag_id = db.Column(db.Integer, primary_key=True)
	turtle_id = db.Column(db.ForeignKey('turtle.turtle_id'), nullable=False)
	tag_number = db.Column(db.String(30))
	location = db.Column(db.String(2))
	active = db.Column(db.Boolean)
	tag_type = db.Column(db.String(30))

class Clutch(db.Model):
	clutch_id = db.Column(db.Integer, primary_key=True)
	turtle_id = db.Column(db.Integer, db.ForeignKey('turtle.turtle_id'), nullable=False)
	hatchlings = db.relationship('Hatchlings', backref='clutch')
	eggs = db.relationship('Eggs', backref='clutch')
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

class Morphometrics(db.Model):
	morphometrics_id = db.Column(db.Integer, primary_key=True)
	turtle_id = db.Column(db.Integer, db.ForeignKey('turtle.turtle_id'), nullable=False)
	encounter_id = db.Column(db.Integer, db.ForeignKey('encounter.encounter_id'), nullable=False)
	encounter = db.relationship('Encounter', back_populates='morphometrics')
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

class Metadata(db.Model):
	metadata_id = db.Column(db.Integer, primary_key=True)
	encounters = db.relationship('Encounter', backref='metadata')
	nets = db.relationship('Net', backref='metadata', lazy=True)
	incidental_captures = db.relationship('IncidentalCapture', backref='metadata')
	environment = db.relationship('Environment', uselist=False, backref='metadata')
	metadata_date = db.Column(db.Date)
	metadata_location = db.Column(db.Text)
	metadata_investigators = db.Column(db.Text)
	number_of_cc_captured = db.Column(db.Integer)
	number_of_cm_captured = db.Column(db.Integer)
	number_of_other_captured = db.Column(db.Integer)

class Encounter(db.Model):
	encounter_id = db.Column(db.Integer, primary_key=True)
	samples = db.relationship('Sample', backref='encounter')
	paps = db.relationship('Paps', uselist=False, lazy=True, back_populates='encounter')
	morphometrics = db.relationship('Morphometrics', uselist=False, back_populates='encounter')
	type = db.Column(db.String(30))

	# Foreign keys
	metadata_id = db.Column(db.Integer, db.ForeignKey('metadata.metadata_id'), nullable=False)
	turtle_id = db.Column(db.Integer, db.ForeignKey('turtle.turtle_id'), nullable=False)

	# Fields common to all encounter types
	encounter_date = db.Column(db.Date)
	encounter_time = db.Column(db.Time)
	species = db.Column(db.String(30))
	investigated_by = db.Column(db.String(30))
	entered_by = db.Column(db.String(30))
	entered_date = db.Column(db.Date)
	verified_by = db.Column(db.String(30))
	verified_date = db.Column(db.Date)

	# Polymorphism
	__mapper_args__ = {
		'polymorphic_identity': 'encounters',
		'polymorphic_on': type
	}

class Sample(db.Model):
	samples_id = db.Column(db.Integer, primary_key=True)
	encounter_id = db.Column(db.Integer, db.ForeignKey('encounter.encounter_id'), nullable=False)
	skin_1 = db.Column(db.Boolean)
	skin_1_for = db.Column(db.Text)
	skin_2 = db.Column(db.Boolean)
	skin_2_for = db.Column(db.Text)
	blood = db.Column(db.Boolean)
	blood_for = db.Column(db.Text)
	scute = db.Column(db.Boolean)
	scute_for = db.Column(db.Text)
	other = db.Column(db.Boolean)
	other_for = db.Column(db.Text)

class Paps(db.Model):
	pap_id = db.Column(db.Integer, primary_key=True)
	encounter_id = db.Column(db.Integer, db.ForeignKey('encounter.encounter_id'), nullable=False)
	encounter = db.relationship('Encounter', back_populates='paps')
	paps_present = db.Column(db.Boolean)
	number_of_paps = db.Column(db.Integer)
	paps_regression = db.Column(db.String(40))
	photos = db.Column(db.Boolean)
	pap_photos = db.Column(db.Boolean)

class TridentEncounter(Encounter):
	# Primary key
	trident_encounter_id = db.Column(db.Integer, primary_key=True)

	# Foreign key
	encounter_id = db.Column(db.Integer, db.ForeignKey('encounter.encounter_id'), nullable=False)
	
	# Fields unique to trident encounters
	capture_location = db.Column(db.String(50))
	capture_method = db.Column(db.String(50))
	number_on_carapace = db.Column(db.Integer)
	living_tags = db.Column(db.Boolean)
	other = db.Column(db.Text)
	leeches = db.Column(db.Boolean)
	leeches_where = db.Column(db.Text)
	leech_eggs = db.Column(db.Boolean)
	leech_eggs_where = db.Column(db.Text)
	disposition_of_specimen = db.Column(db.Text)

	# Polymorphism
	__mapper_args__ = {
		'polymorphic_identity': 'trident'
	}

class LagoonEncounter(Encounter):
	# Primary key
	lagoon_encounter_id = db.Column(db.Integer, primary_key=True)

	# Foreign key
	encounter_id = db.Column(db.Integer, db.ForeignKey('encounter.encounter_id'), nullable=False)

	# Fields unique to lagoon encounters
	living_tags = db.Column(db.Boolean)
	other = db.Column(db.Text)
	leeches = db.Column(db.Boolean)
	leeches_where = db.Column(db.Text)
	leech_eggs = db.Column(db.Boolean)
	leech_eggs_where = db.Column(db.Text)

	# Polymorphism
	__mapper_args__ = {
		'polymorphic_identity': 'lagoon'
	}

class BeachEncounter(Encounter):
	# Primary key
	beach_encounter_id = db.Column(db.Integer, primary_key=True)

	# Foreign key
	encounter_id = db.Column(db.Integer, db.ForeignKey('encounter.encounter_id'), nullable=False)

	# Things that depend on this table
	beach_dc_data = db.relationship('BeachDcData', backref='encounter', lazy=True, uselist=False)
	nest_markings = db.relationship('NestMarking', backref='encounter', lazy=True, uselist=False)

	# Fields unique to beach encounters
	days_45 = db.Column(db.Date)
	days_70 = db.Column(db.Date)
	capture_type = db.Column(db.String(40))
	activity = db.Column(db.String(50))
	location = db.Column(db.Float(5))
	location_NS = db.Column(db.String(1))
	lat_n = db.Column(db.Float(5))
	lat_w = db.Column(db.Float(5))
	site_description = db.Column(db.Text)
	notes = db.Column(db.Text)

	# Polymorphism
	__mapper_args__ = {
		'polymorphic_identity': 'beach'
	}

class BeachDcData(db.Model):
	beach_dc_data_id = db.Column(db.Integer, primary_key=True)
	beach_encounter_id = db.Column(db.Integer, db.ForeignKey('beach_encounter.beach_encounter_id'), nullable=False)
	outgoing_crawl_width = db.Column(db.Float(5))
	yolkless_collected = db.Column(db.Boolean)
	pink_spot_photo_taken = db.Column(db.Boolean)
	photo_taken_by = db.Column(db.Text)

class NestMarking(db.Model):
	nest_marking_id = db.Column(db.Integer, primary_key=True)
	beach_encounter_id = db.Column(db.Integer, db.ForeignKey('beach_encounter.beach_encounter_id'), nullable=False)
	dist_to_hidden_stake = db.Column(db.Float(5))
	hidden_stake_planted_in = db.Column(db.Text)
	dist_to_obvious_stake = db.Column(db.Float(5))
	obvious_stake_planted_in = db.Column(db.Text)
	dist_to_dune = db.Column(db.Float(5))
	dist_to_high_tide = db.Column(db.Float(5))
	can_buried = db.Column(db.Boolean)
	can_buried_NS = db.Column(db.String(1))
	scarp_over_46_cm = db.Column(db.Boolean)
	seaward_of_structure = db.Column(db.Boolean)
	within_1_m_of_structure = db.Column(db.Boolean)
	structure_description = db.Column(db.Text)

class Net(db.Model):
	net_id = db.Column(db.Integer, primary_key=True)
	metadata_id = db.Column(db.Integer, db.ForeignKey('metadata.metadata_id'), nullable=False)
	net_number = db.Column(db.Integer)
	net_deploy_start_time = db.Column(db.Time)
	net_deploy_end_time = db.Column(db.Time)
	net_retrieval_start_time = db.Column(db.Time)
	net_retrieval_end_time = db.Column(db.Time)

class IncidentalCapture(db.Model):
	incidental_capture_id = db.Column(db.Integer, primary_key=True)
	metadata_id = db.Column(db.Integer, db.ForeignKey('metadata.metadata_id'), nullable=False)
	species = db.Column(db.String(40))
	capture_time = db.Column(db.Time)
	measurement = db.Column(db.Text)
	notes = db.Column(db.Text)

class Environment(db.Model):
	environment_id = db.Column(db.Integer, primary_key=True)
	metadata_id = db.Column(db.Integer, db.ForeignKey('metadata.metadata_id'), nullable=False)
	water_sample = db.Column(db.Boolean)
	wind_speed = db.Column(db.Float(5))
	wind_dir = db.Column(db.String(20))
	environment_time = db.Column(db.Time)
	weather = db.Column(db.String(100))
	air_temp = db.Column(db.Float(5))
	water_temp_surface = db.Column(db.Float(5))
	water_temp_1_m = db.Column(db.Float(5))
	water_temp_2_m = db.Column(db.Float(5))
	water_temp_6_m = db.Column(db.Float(5))
	water_temp_bottom = db.Column(db.Float(5))
	salinity_surface = db.Column(db.Float(5))
	salinity_1_m = db.Column(db.Float(5))
	salinity_2_m = db.Column(db.Float(5))
	salinity_6_m = db.Column(db.Float(5))
	salinity_bottom = db.Column(db.Float(5))

class TurtleSchema(ma.ModelSchema):
	class Meta:
		model = Turtle

class TagSchema(ma.ModelSchema):
	class Meta:
		model = Tag

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

class EncounterSchema(ma.ModelSchema):
	class Meta:
		model = Encounter

class SampleSchema(ma.ModelSchema):
	class Meta:
		model = Sample

class PapsSchema(ma.ModelSchema):
	class Meta:
		model = Paps

class TridentEncounterSchema(ma.ModelSchema):
	class Meta:
		model = TridentEncounter

class LagoonEncounterSchema(ma.ModelSchema):
	class Meta:
		model = LagoonEncounter

class BeachEncounterSchema(ma.ModelSchema):
	class Meta:
		model = BeachEncounter

class BeachDcDataSchema(ma.ModelSchema):
	class Meta:
		model = BeachDcData

class NestMarkingSchema(ma.ModelSchema):
	class Meta:
		model = NestMarking

class MetadataSchema(ma.ModelSchema):
	class Meta:
		model = Metadata

class NetSchema(ma.ModelSchema):
	class Meta:
		model = Net

class IncidentalCaptureSchema(ma.ModelSchema):
	class Meta:
		model = IncidentalCapture

class EnvironmentSchema(ma.ModelSchema):
	class Meta:
		model = Environment

