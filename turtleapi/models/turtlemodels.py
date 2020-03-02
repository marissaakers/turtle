from turtleapi import db, ma
from flask import jsonify
from marshmallow import Schema, fields, pre_dump, post_dump
from sqlathanor import declarative_base, Column, relationship
from datetime import datetime
from sqlalchemy.orm import backref

BaseModel = declarative_base()

def parse_time(value):
	if value is None:
		return value
	return datetime.strptime(value, '%H:%M:%S')

class Turtle(BaseModel):
	__tablename__ = 'turtle'
	# Primary key
	turtle_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)

	# Dependencies
	tags = relationship('Tag', backref='turtle', supports_dict=True, supports_json=True)
	clutches = relationship('Clutch', backref='turtle', supports_dict=True, supports_json=True)
	encounters = relationship('Encounter', backref='turtle', lazy='dynamic', supports_dict=True, supports_json=True)	

	# Various fields
	species = Column(db.String(30), supports_dict=True, supports_json=True)
	old_turtle_id = Column(db.Integer, supports_dict=True, supports_json=True)

class Tag(BaseModel):
	__tablename__ = 'tag'
	# Primary key
	tag_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)
	
	# Foreign key
	turtle_id = Column(db.ForeignKey('turtle.turtle_id'), nullable=False, supports_dict=True, supports_json=True)

	# Various fields
	tag_number = Column(db.String(30), supports_dict=True, supports_json=True)
	tag_scars = Column(db.Boolean, supports_dict=True, supports_json=True)
	active = Column(db.Boolean, supports_dict=True, supports_json=True)
	tag_type = Column(db.String(30), supports_dict=True, supports_json=True)
	pit = Column(db.Boolean, supports_dict=True, supports_json=True)
	scanned = Column(db.Boolean, supports_dict=True, supports_json=True)
	scanner_number = Column(db.String(30), supports_dict=True, supports_json=True)

class Clutch(BaseModel):
	__tablename__ = 'clutch'
	# Primary key
	clutch_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)
	
	# Foreign key
	turtle_id = Column(db.Integer, db.ForeignKey('turtle.turtle_id'), nullable=False, supports_dict=True, supports_json=True)

	# Various fields
	stake_number = Column(db.String(30), supports_dict=True, supports_json=True)
	clutch_deposited = Column(db.Boolean, supports_dict=True, supports_json=True)
	sand_type = Column(db.String(50), supports_dict=True, supports_json=True)
	placement = Column(db.String(50), supports_dict=True, supports_json=True)
	emergence_date = Column(db.Date, supports_dict=True, supports_json=True)
	inventory_date = Column(db.Date, supports_dict=True, supports_json=True)
	hidden_stake_in_place = Column(db.Boolean, supports_dict=True, supports_json=True)
	obvious_stake_in_place = Column(db.Boolean, supports_dict=True, supports_json=True)
	emergence = Column(db.Boolean, supports_dict=True, supports_json=True)
	s_can_in_place = Column(db.Boolean, supports_dict=True, supports_json=True)
	n_can_in_place = Column(db.Boolean, supports_dict=True, supports_json=True)
	predated = Column(db.Boolean, supports_dict=True, supports_json=True)
	post_hatch = Column(db.Boolean, supports_dict=True, supports_json=True)
	washed_over = Column(db.Boolean, supports_dict=True, supports_json=True)
	inundated = Column(db.Boolean, supports_dict=True, supports_json=True)
	washed_out = Column(db.String(20), supports_dict=True, supports_json=True)
	washed_out_post_hatch = Column(db.Boolean, supports_dict=True, supports_json=True)
	poached = Column(db.Boolean, supports_dict=True, supports_json=True)
	inventoried_by = Column(db.String(500), supports_dict=True, supports_json=True)
	entered_by = Column(db.String(40), supports_dict=True, supports_json=True)
	entered_date = Column(db.Date, supports_dict=True, supports_json=True)
	verified_by = Column(db.String(40), supports_dict=True, supports_json=True)
	verified_date = Column(db.Date, supports_dict=True, supports_json=True)
	
	# Hatchlings
	hatched = Column(db.Integer, supports_dict=True, supports_json=True)
	live_hatchlings = Column(db.Integer, supports_dict=True, supports_json=True)
	dead_hatchlings = Column(db.Integer, supports_dict=True, supports_json=True)
	hatchlings_emerged = Column(db.Integer, supports_dict=True, supports_json=True)
	pipped_live = Column(db.Integer, supports_dict=True, supports_json=True)
	pipped_dead = Column(db.Integer, supports_dict=True, supports_json=True)
	
	# Eggs
	eggs_addled = Column(db.Integer, supports_dict=True, supports_json=True)
	eggs_undeveloped = Column(db.Integer, supports_dict=True, supports_json=True)
	eggs_sampled_for_sac = Column(db.Integer, supports_dict=True, supports_json=True)
	eggs_embryo_1_4 = Column(db.Integer, supports_dict=True, supports_json=True)
	eggs_embryo_2_4 = Column(db.Integer, supports_dict=True, supports_json=True)
	eggs_embryo_3_4 = Column(db.Integer, supports_dict=True, supports_json=True)
	eggs_embryo_4_4 = Column(db.Integer, supports_dict=True, supports_json=True)
	eggs_damaged_raccoons = Column(db.Integer, supports_dict=True, supports_json=True)
	eggs_damaged_ghost_crabs = Column(db.Integer, supports_dict=True, supports_json=True)
	egg_damaged_plant_roots = Column(db.Integer, supports_dict=True, supports_json=True)
	eggs_damaged_another_turtle = Column(db.Integer, supports_dict=True, supports_json=True)
	eggs_damaged_bobcat = Column(db.Integer, supports_dict=True, supports_json=True)
	eggs_damaged_other = Column(db.Integer, supports_dict=True, supports_json=True)
	eggs_damaged_sea_oats = Column(db.Boolean, supports_dict=True, supports_json=True)
	eggs_damaged_sea_purslane = Column(db.Boolean, supports_dict=True, supports_json=True)
	eggs_damaged_railroad_vine = Column(db.Boolean, supports_dict=True, supports_json=True)
	eggs_damaged_beach_sunflower = Column(db.Boolean, supports_dict=True, supports_json=True)
	eggs_damaged_sea_grape = Column(db.Boolean, supports_dict=True, supports_json=True)
	eggs_broken = Column(db.Integer, supports_dict=True, supports_json=True)
	eggs_washout = Column(db.Integer, supports_dict=True, supports_json=True)
	eggs_other = Column(db.Integer, supports_dict=True, supports_json=True)
	eggs_other_details = Column(db.Text, supports_dict=True, supports_json=True)
	eggs_yolkless_hydrated = Column(db.Integer, supports_dict=True, supports_json=True)
	eggs_yolkless_dehydrated = Column(db.Integer, supports_dict=True, supports_json=True)
	clutch_size = Column(db.Integer, supports_dict=True, supports_json=True)
	substrate = Column(db.String(50), supports_dict=True, supports_json=True)
	notes = Column(db.Text, supports_dict=True, supports_json=True)

class Morphometrics(BaseModel):
	__tablename__ = 'morphometrics'
	# Primary key
	morphometrics_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)

	# Foreign keys
	encounter_id = Column(db.Integer, db.ForeignKey('encounter.encounter_id'), nullable=False, supports_dict=True, supports_json=True)

	# Various fields
	curved_length = Column(db.Float(5), supports_dict=True, supports_json=True)
	straight_length = Column(db.Float(5), supports_dict=True, supports_json=True)
	minimum_length = Column(db.Float(5), supports_dict=True, supports_json=True)
	plastron_length = Column(db.Float(5), supports_dict=True, supports_json=True)
	weight = Column(db.Float(5), supports_dict=True, supports_json=True)
	curved_width = Column(db.Float(5), supports_dict=True, supports_json=True)
	straight_width = Column(db.Float(5), supports_dict=True, supports_json=True)
	tail_length_pl_vent = Column(db.Float(5), supports_dict=True, supports_json=True)
	tail_length_pl_tip = Column(db.Float(5), supports_dict=True, supports_json=True)
	head_width = Column(db.Float(5), supports_dict=True, supports_json=True)
	body_depth = Column(db.Float(5), supports_dict=True, supports_json=True)
	flipper_damage = Column(db.Text, supports_dict=True, supports_json=True)
	carapace_damage = Column(db.Text, supports_dict=True, supports_json=True)

class Metadata(BaseModel):
	__tablename__ = 'metadata'
	# Primary key
	metadata_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)

	# Dependencies
	encounters = relationship('Encounter', backref='metadata', supports_dict=True, supports_json=True)
	nets = relationship('Net', backref='metadata', lazy=True, supports_dict=True, supports_json=True)
	incidental_captures = relationship('IncidentalCapture', backref='metadata', supports_dict=True, supports_json=True)

	# Polymorphism
	type = Column(db.String(30), supports_dict=True, supports_json=True)
	__mapper_args__ = {
		'polymorphic_identity': 'metadatas',
		'polymorphic_on': type
	}

class LagoonMetadata(Metadata):
	__tablename__ = 'lagoon_metadata'
	# Foreign key
	metadata_id = Column(db.Integer, db.ForeignKey('metadata.metadata_id'),primary_key=True, nullable=False, supports_dict=True, supports_json=True)

	# Various fields
	metadata_date = Column(db.Date, supports_dict=True, supports_json=True)
	metadata_location = Column(db.Text, supports_dict=True, supports_json=True)
	metadata_investigators = Column(db.Text, supports_dict=True, supports_json=True)
	number_of_cc_captured = Column(db.Integer, supports_dict=True, supports_json=True)
	number_of_cm_captured = Column(db.Integer, supports_dict=True, supports_json=True)
	number_of_other_captured = Column(db.Integer, supports_dict=True, supports_json=True)

	# Environment
	water_sample = Column(db.Boolean, supports_dict=True, supports_json=True)
	wind_speed = Column(db.Float(5), supports_dict=True, supports_json=True)
	wind_dir = Column(db.String(20), supports_dict=True, supports_json=True)
	environment_time = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time)
	weather = Column(db.String(100), supports_dict=True, supports_json=True)
	air_temp = Column(db.Float(5), supports_dict=True, supports_json=True)
	water_temp_surface = Column(db.Float(5), supports_dict=True, supports_json=True)
	water_temp_1_m = Column(db.Float(5), supports_dict=True, supports_json=True)
	water_temp_2_m = Column(db.Float(5), supports_dict=True, supports_json=True)
	water_temp_6_m = Column(db.Float(5), supports_dict=True, supports_json=True)
	water_temp_bottom = Column(db.Float(5), supports_dict=True, supports_json=True)
	salinity_surface = Column(db.Float(5), supports_dict=True, supports_json=True)
	salinity_1_m = Column(db.Float(5), supports_dict=True, supports_json=True)
	salinity_2_m = Column(db.Float(5), supports_dict=True, supports_json=True)
	salinity_6_m = Column(db.Float(5), supports_dict=True, supports_json=True)
	salinity_bottom = Column(db.Float(5), supports_dict=True, supports_json=True)

	# Polymorphism
	__mapper_args__ = {
		'polymorphic_identity': 'lagoon'
	}

class TridentMetadata(Metadata):
	__tablename__ = 'trident_metadata'
	# Foreign key
	metadata_id = Column(db.Integer, db.ForeignKey('metadata.metadata_id'), primary_key=True, nullable=False, supports_dict=True, supports_json=True)

	# Various fields
	metadata_date = Column(db.Date, supports_dict=True, supports_json=True)
	metadata_location = Column(db.Text, supports_dict=True, supports_json=True)
	metadata_investigators = Column(db.Text, supports_dict=True, supports_json=True)
	number_of_cc_captured = Column(db.Integer, supports_dict=True, supports_json=True)
	number_of_cm_captured = Column(db.Integer, supports_dict=True, supports_json=True)
	number_of_other_captured = Column(db.Integer, supports_dict=True, supports_json=True)

	# Environment
	water_sample = Column(db.Boolean, supports_dict=True, supports_json=True)
	wind_speed = Column(db.Float(5), supports_dict=True, supports_json=True)
	wind_dir = Column(db.String(20), supports_dict=True, supports_json=True)
	environment_time = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time)
	weather = Column(db.String(100), supports_dict=True, supports_json=True)
	air_temp = Column(db.Float(5), supports_dict=True, supports_json=True)
	water_temp_surface = Column(db.Float(5), supports_dict=True, supports_json=True)
	water_temp_1_m = Column(db.Float(5), supports_dict=True, supports_json=True)
	water_temp_2_m = Column(db.Float(5), supports_dict=True, supports_json=True)
	water_temp_6_m = Column(db.Float(5), supports_dict=True, supports_json=True)
	water_temp_bottom = Column(db.Float(5), supports_dict=True, supports_json=True)
	salinity_surface = Column(db.Float(5), supports_dict=True, supports_json=True)
	salinity_1_m = Column(db.Float(5), supports_dict=True, supports_json=True)
	salinity_2_m = Column(db.Float(5), supports_dict=True, supports_json=True)
	salinity_6_m = Column(db.Float(5), supports_dict=True, supports_json=True)
	salinity_bottom = Column(db.Float(5), supports_dict=True, supports_json=True)

	# Polymorphism
	__mapper_args__ = {
		'polymorphic_identity': 'trident'
	}

class OffshoreMetadata(Metadata):
	__tablename__ = 'offshore_metadata'
	# Foreign key
	metadata_id = Column(db.Integer, db.ForeignKey('metadata.metadata_id'), primary_key=True, nullable=False, supports_dict=True, supports_json=True)

	# Capture
	capture_date = Column(db.Date, supports_dict=True, supports_json=True)
	capture_time = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time)
	capture_latitude = Column(db.Float(5), supports_dict=True, supports_json=True)
	capture_longitude = Column(db.Float(5), supports_dict=True, supports_json=True)
	cloud_cover = Column(db.Text, supports_dict=True, supports_json=True)
	seas = Column(db.Text, supports_dict=True, supports_json=True)
	wind = Column(db.Text, supports_dict=True, supports_json=True)
	capture_sargassum_water_temp = Column(db.Float(5), supports_dict=True, supports_json=True)
	capture_open_water_temp = Column(db.Float(5), supports_dict=True, supports_json=True)
	capture_air_temp = Column(db.Float(5), supports_dict=True, supports_json=True)

	# Release
	release_latitude = Column(db.Float(5), supports_dict=True, supports_json=True)
	release_longitude = Column(db.Float(5), supports_dict=True, supports_json=True)
	release_time = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time)
	release_sargassum_water_temp = Column(db.Float(5), supports_dict=True, supports_json=True)
	sargassum_salinity = Column(db.Float(5), supports_dict=True, supports_json=True)
	release_air_temp = Column(db.Float(5), supports_dict=True, supports_json=True)
	release_open_water_temp = Column(db.Float(5), supports_dict=True, supports_json=True)
	open_water_salinity = Column(db.Float(5), supports_dict=True, supports_json=True)
	drifter_released = Column(db.Boolean, supports_dict=True, supports_json=True)
	drifter1_id = Column(db.Text, supports_dict=True, supports_json=True)
	drifter2_id = Column(db.Text, supports_dict=True, supports_json=True)
	drifter1_type = Column(db.Text, supports_dict=True, supports_json=True)
	drifter2_type = Column(db.Text, supports_dict=True, supports_json=True)

	# Polymorphism
	__mapper_args__ = {
		'polymorphic_identity': 'offshore'
	}

class Encounter(BaseModel):
	__tablename__ = 'encounter'
	# Primary key
	encounter_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)

	# Foreign keys
	metadata_id = Column(db.Integer, db.ForeignKey('metadata.metadata_id'))
	turtle_id = Column(db.Integer, db.ForeignKey('turtle.turtle_id'), nullable=False, supports_dict=True, supports_json=True)

	# Dependencies
	samples = relationship('Sample', backref='encounter', supports_dict=True, supports_json=True)
	morphometrics = relationship('Morphometrics', backref=backref('encounter', uselist=False), supports_dict=True, supports_json=True)

	# Polymorphism
	type = Column(db.String(30), supports_dict=True, supports_json=True)
	__mapper_args__ = {
		'polymorphic_identity': 'encounters',
		'polymorphic_on': type
	}

class Sample(BaseModel):
	__tablename__ = 'sample'
	# Primary key
	sample_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)

	# Foreign key
	encounter_id = Column(db.Integer, db.ForeignKey('encounter.encounter_id'), nullable=False, supports_dict=True, supports_json=True)

	# Dependencies
	tracking_entries = relationship('SampleTracking', backref='sample', lazy='joined', supports_dict=True, supports_json=True)

	# Various fields
	skin_1 = Column(db.Boolean, supports_dict=True, supports_json=True)
	skin_1_for = Column(db.Text, supports_dict=True, supports_json=True)
	skin_2 = Column(db.Boolean, supports_dict=True, supports_json=True)
	skin_2_for = Column(db.Text, supports_dict=True, supports_json=True)
	blood = Column(db.Boolean, supports_dict=True, supports_json=True)
	blood_for = Column(db.Text, supports_dict=True, supports_json=True)
	scute = Column(db.Boolean, supports_dict=True, supports_json=True)
	scute_for = Column(db.Text, supports_dict=True, supports_json=True)
	other = Column(db.Boolean, supports_dict=True, supports_json=True)
	other_for = Column(db.Text, supports_dict=True, supports_json=True)

class TridentEncounter(Encounter):
	__tablename__ = 'trident_encounter'
	# Primary key
	encounter_id = Column(db.Integer, db.ForeignKey('encounter.encounter_id'), primary_key=True, nullable=False, supports_dict=True, supports_json=True)
	
	# Fields common to all encounter types
	encounter_date = Column(db.Date, supports_dict=True, supports_json=True)
	encounter_time = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time)
	capture_type = Column(db.String(40), supports_dict=True, supports_json=True)
	investigated_by = Column(db.String(500), supports_dict=True, supports_json=True)
	entered_by = Column(db.String(30), supports_dict=True, supports_json=True)
	entered_date = Column(db.Date, supports_dict=True, supports_json=True)
	verified_by = Column(db.String(30), supports_dict=True, supports_json=True)
	verified_date = Column(db.Date, supports_dict=True, supports_json=True)
	notes = Column(db.Text, supports_dict=True, supports_json=True)


	# Fields unique to trident encounters
	capture_location = Column(db.String(50), supports_dict=True, supports_json=True)
	capture_method = Column(db.String(50), supports_dict=True, supports_json=True)
	number_on_carapace = Column(db.Integer, supports_dict=True, supports_json=True)
	living_tags = Column(db.Boolean, supports_dict=True, supports_json=True)
	other = Column(db.Text, supports_dict=True, supports_json=True)
	leeches = Column(db.Boolean, supports_dict=True, supports_json=True)
	leeches_where = Column(db.Text, supports_dict=True, supports_json=True)
	leech_eggs = Column(db.Boolean, supports_dict=True, supports_json=True)
	leech_eggs_where = Column(db.Text, supports_dict=True, supports_json=True)
	disposition_of_specimen = Column(db.Text, supports_dict=True, supports_json=True)

	# Paps
	paps_present = Column(db.Boolean, supports_dict=True, supports_json=True)
	pap_category = Column(db.Integer, supports_dict=True, supports_json=True)
	paps_regression = Column(db.String(40), supports_dict=True, supports_json=True)
	photos = Column(db.Boolean, supports_dict=True, supports_json=True)
	pap_photos = Column(db.Boolean, supports_dict=True, supports_json=True)

	# Polymorphism
	__mapper_args__ = {
		'polymorphic_identity': 'trident'
	}

class LagoonEncounter(Encounter):
	__tablename__ = 'lagoon_encounter'
	# Primary key
	encounter_id = Column(db.Integer, db.ForeignKey('encounter.encounter_id'), primary_key=True, nullable=False, supports_dict=True, supports_json=True)

	# Fields common to all encounter types
	encounter_date = Column(db.Date, supports_dict=True, supports_json=True)
	encounter_time = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time)
	capture_type = Column(db.String(40), supports_dict=True, supports_json=True)
	investigated_by = Column(db.String(500), supports_dict=True, supports_json=True)
	entered_by = Column(db.String(30), supports_dict=True, supports_json=True)
	entered_date = Column(db.Date, supports_dict=True, supports_json=True)
	verified_by = Column(db.String(30), supports_dict=True, supports_json=True)
	verified_date = Column(db.Date, supports_dict=True, supports_json=True)
	notes = Column(db.Text, supports_dict=True, supports_json=True)


	# Paps
	paps_present = Column(db.Boolean, supports_dict=True, supports_json=True)
	pap_category = Column(db.Integer, supports_dict=True, supports_json=True)
	paps_regression = Column(db.String(40), supports_dict=True, supports_json=True)
	photos = Column(db.Boolean, supports_dict=True, supports_json=True)
	pap_photos = Column(db.Boolean, supports_dict=True, supports_json=True)

	# Fields unique to lagoon encounters
	living_tags = Column(db.Boolean, supports_dict=True, supports_json=True)
	other = Column(db.Text, supports_dict=True, supports_json=True)
	leeches = Column(db.Boolean, supports_dict=True, supports_json=True)
	leeches_where = Column(db.Text, supports_dict=True, supports_json=True)
	leech_eggs = Column(db.Boolean, supports_dict=True, supports_json=True)
	leech_eggs_where = Column(db.Text, supports_dict=True, supports_json=True)

	# Polymorphism
	__mapper_args__ = {
		'polymorphic_identity': 'lagoon'
	}

class BeachEncounter(Encounter):
	__tablename__ = 'beach_encounter'
	# Primary key
	encounter_id = Column(db.Integer, db.ForeignKey('encounter.encounter_id'), primary_key=True, nullable=False, supports_dict=True, supports_json=True)

	# Fields common to all encounter types
	encounter_date = Column(db.Date, supports_dict=True, supports_json=True)
	encounter_time = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time)
	capture_type = Column(db.String(40), supports_dict=True, supports_json=True)
	investigated_by = Column(db.String(500), supports_dict=True, supports_json=True)
	entered_by = Column(db.String(30), supports_dict=True, supports_json=True)
	entered_date = Column(db.Date, supports_dict=True, supports_json=True)
	verified_by = Column(db.String(30), supports_dict=True, supports_json=True)
	verified_date = Column(db.Date, supports_dict=True, supports_json=True)

	# Fields unique to beach encounters
	prime_tag = Column(db.String(30), supports_dict=True, supports_json=True)
	days_45 = Column(db.Date, supports_dict=True, supports_json=True)
	days_70 = Column(db.Date, supports_dict=True, supports_json=True)
	activity = Column(db.String(50), supports_dict=True, supports_json=True)
	location_detail = Column(db.Text, supports_dict=True, supports_json=True)
	location_NS = Column(db.String(1), supports_dict=True, supports_json=True)
	latitude = Column(db.Float(5), supports_dict=True, supports_json=True)
	longitude = Column(db.Float(5), supports_dict=True, supports_json=True)
	site_description = Column(db.Text, supports_dict=True, supports_json=True)
	notes = Column(db.Text, supports_dict=True, supports_json=True)

	# DC Data
	outgoing_crawl_width = Column(db.Float(5), supports_dict=True, supports_json=True)
	yolkless_collected = Column(db.Boolean, supports_dict=True, supports_json=True)
	pink_spot_photo_taken = Column(db.Boolean, supports_dict=True, supports_json=True)
	photo_taken_by = Column(db.Text, supports_dict=True, supports_json=True)

	# Nest Markings
	dist_to_hidden_stake = Column(db.Float(5), supports_dict=True, supports_json=True)
	hidden_stake_planted_in = Column(db.Text, supports_dict=True, supports_json=True)
	dist_to_obvious_stake = Column(db.Float(5), supports_dict=True, supports_json=True)
	obvious_stake_planted_in = Column(db.Text, supports_dict=True, supports_json=True)
	dist_to_dune = Column(db.Float(5), supports_dict=True, supports_json=True)
	dist_to_high_tide = Column(db.Float(5), supports_dict=True, supports_json=True)
	can_buried = Column(db.Boolean, supports_dict=True, supports_json=True)
	can_buried_NS = Column(db.String(1), supports_dict=True, supports_json=True)
	sign_stake_in_place = Column(db.Boolean, supports_dict=True, supports_json=True)
	scarp_over_46_cm = Column(db.Boolean, supports_dict=True, supports_json=True)
	seaward_of_structure = Column(db.Boolean, supports_dict=True, supports_json=True)
	within_1_m_of_structure = Column(db.Boolean, supports_dict=True, supports_json=True)
	structure_description = Column(db.Text, supports_dict=True, supports_json=True)

	# Paps
	paps_present = Column(db.Boolean, supports_dict=True, supports_json=True)

	# Polymorphism
	__mapper_args__ = {
		'polymorphic_identity': 'beach'
	}

class Net(BaseModel):
	__tablename__ = 'net'
	# Primary key
	net_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)
	
	# Foreign key
	metadata_id = Column(db.Integer, db.ForeignKey('metadata.metadata_id'), nullable=False, supports_dict=True, supports_json=True)

	# Various fields
	net_number = Column(db.Integer, supports_dict=True, supports_json=True)
	net_deploy_start_time = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time)
	net_deploy_end_time = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time)
	net_retrieval_start_time = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time)
	net_retrieval_end_time = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time)
	loggerhead_captures = Column(db.Integer, supports_dict=True, supports_json=True)
	green_captures = Column(db.Integer, supports_dict=True, supports_json=True)
	entered_by = Column(db.Text, supports_dict=True, supports_json=True)
	green_cpue = Column(db.Float(5), supports_dict=True, supports_json=True)
	loggerhead_cpue = Column(db.Float(5), supports_dict=True, supports_json=True)
	net_kilometers = Column(db.Float(5), supports_dict=True, supports_json=True)
	net_km_hours = Column(db.Float(5), supports_dict=True, supports_json=True)
	net_type = Column(db.String(30), supports_dict=True, supports_json=True)
	soak_time = Column(db.Float(5), supports_dict=True, supports_json=True)

class IncidentalCapture(BaseModel):
	__tablename__ = 'incidental_capture'
	# Primary key
	incidental_capture_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)

	# Foreign key
	metadata_id = Column(db.Integer, db.ForeignKey('metadata.metadata_id'), nullable=False, supports_dict=True, supports_json=True)

	# Various fields
	species = Column(db.String(40), supports_dict=True, supports_json=True)
	capture_time = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time)
	measurement = Column(db.Text, supports_dict=True, supports_json=True)
	notes = Column(db.Text, supports_dict=True, supports_json=True)

class SampleTracking(BaseModel):
	__tablename__ = 'sample_tracking'
	# Primary key
	sample_tracking_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)

	# Foreign key
	sample_id = Column(db.Integer, db.ForeignKey('sample.sample_id'), nullable=False, supports_dict=True, supports_json=True)

	# Fields
	date = Column(db.Date, supports_dict=True, supports_json=True)
	notes = Column(db.Text, supports_dict=True, supports_json=True)

class NSRefuge(BaseModel):
	__tablename__ = 'ns_refuge'
	# Primary key
	ns_refuge_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)

	# Dependencies
	# encounters = relationship('Encounter', backref='metadata', supports_dict=True, supports_json=True)
	dc_crawls = relationship('DcCrawl', backref='ns_refuge', supports_dict=True, supports_json=True)
	disorientations = relationship('Disorientation', backref='ns_refuge', supports_dict=True, supports_json=True)
	depredations = relationship('Depredation', backref='ns_refuge', supports_dict=True, supports_json=True)

	# Fields
	type = Column(db.String(10), supports_dict=True, supports_json=True)
	date = Column(db.Date, supports_dict=True, supports_json=True)
	initials = Column(db.String(30), supports_dict=True, supports_json=True)
	notes = Column(db.Text, supports_dict=True, supports_json=True)

	# # Km Fields
	# km_start = Column(db.Float(5), supports_dict=True, supports_json=True)
	# km_end = Column(db.Float(5), supports_dict=True, supports_json=True)
	# cc_nests = Column(postgresql.ARRAY(db.Integer, supports_dict=True, supports_json=True),server_default='[]', supports_dict=True, supports_json=True)
	# cc_fc = Column(postgresql.ARRAY(db.Integer, supports_dict=True, supports_json=True),server_default='[]', supports_dict=True, supports_json=True)
	# cm_nests = Column(postgresql.ARRAY(db.Integer, supports_dict=True, supports_json=True),server_default='[]', supports_dict=True, supports_json=True)
	# cm_fc = Column(postgresql.ARRAY(db.Integer, supports_dict=True, supports_json=True),server_default='[]', supports_dict=True, supports_json=True)

	# # BTO Fields
	# enginr = Column(db.Float(5), supports_dict=True, supports_json=True)
	# natural = Column(db.Float(5), supports_dict=True, supports_json=True)
	# enginr_cc_bto = Column(postgresql.ARRAY(db.Integer, supports_dict=True, supports_json=True),server_default='[]', supports_dict=True, supports_json=True)
	# enginr_cc_bto_lpac = Column(postgresql.ARRAY(db.Integer, supports_dict=True, supports_json=True),server_default='[]', supports_dict=True, supports_json=True)
	# enginr_cm_bto = Column(postgresql.ARRAY(db.Integer, supports_dict=True, supports_json=True),server_default='[]', supports_dict=True, supports_json=True)
	# enginr_cm_bto_lpac = Column(postgresql.ARRAY(db.Integer, supports_dict=True, supports_json=True),server_default='[]', supports_dict=True, supports_json=True)
	# natural_cc_bto = Column(postgresql.ARRAY(db.Integer, supports_dict=True, supports_json=True),server_default='[]', supports_dict=True, supports_json=True)
	# natural_cc_bto_lpac = Column(postgresql.ARRAY(db.Integer, supports_dict=True, supports_json=True),server_default='[]', supports_dict=True, supports_json=True)
	# natural_cm_bto = Column(postgresql.ARRAY(db.Integer, supports_dict=True, supports_json=True),server_default='[]', supports_dict=True, supports_json=True)
	# natural_cm_bto_lpac = Column(postgresql.ARRAY(db.Integer, supports_dict=True, supports_json=True),server_default='[]', supports_dict=True, supports_json=True)

	# Below HTL
	below_htl_cc_nest = Column(db.Integer, supports_dict=True, supports_json=True)
	below_htl_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	below_htl_cm_nest = Column(db.Integer, supports_dict=True, supports_json=True)
	below_htl_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	below_htl_dc_nest = Column(db.Integer, supports_dict=True, supports_json=True)
	below_htl_dc_fc = Column(db.Integer, supports_dict=True, supports_json=True)

	# Km Fields
	km_5_155_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_5_155_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_5_155_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_5_155_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_55_16_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_55_16_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_55_16_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_55_16_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_6_165_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_6_165_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_6_165_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_6_165_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_65_17_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_65_17_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_65_17_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_65_17_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_7_175_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_7_175_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_7_175_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_7_175_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_75_18_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_75_18_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_75_18_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_75_18_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_8_185_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_8_185_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_8_185_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_8_185_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_85_19_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_85_19_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_85_19_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_85_19_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_9_195_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_9_195_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_9_195_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_9_195_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_95_20_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_95_20_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_95_20_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_95_20_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_10_205_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_10_205_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_10_205_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_10_205_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_105_21_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_105_21_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_105_21_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_105_21_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_11_215_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_11_215_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_11_215_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_11_215_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_115_22_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_115_22_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_115_22_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_115_22_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_12_225_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_12_225_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_12_225_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_12_225_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_125_23_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_125_23_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_125_23_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_125_23_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_13_235_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_13_235_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_13_235_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_13_235_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_135_24_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_135_24_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_135_24_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_135_24_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_14_245_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_14_245_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_14_245_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_14_245_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_145_25_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_145_25_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_145_25_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_145_25_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_15_255_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_15_255_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_15_255_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_15_255_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)

	# BTO Fields
	enginr = Column(db.Float(5), supports_dict=True, supports_json=True)
	enginr_cc_below = Column(db.Integer, supports_dict=True, supports_json=True)
	enginr_cc_tran = Column(db.Integer, supports_dict=True, supports_json=True)
	enginr_cc_on = Column(db.Integer, supports_dict=True, supports_json=True)
	enginr_cc_b_l = Column(db.Integer, supports_dict=True, supports_json=True)
	enginr_cc_b_p = Column(db.Integer, supports_dict=True, supports_json=True)
	enginr_cc_b_ac = Column(db.Integer, supports_dict=True, supports_json=True)
	enginr_cc_t_l = Column(db.Integer, supports_dict=True, supports_json=True)
	enginr_cc_t_p = Column(db.Integer, supports_dict=True, supports_json=True)
	enginr_cc_t_ac = Column(db.Integer, supports_dict=True, supports_json=True)
	enginr_cc_o_l = Column(db.Integer, supports_dict=True, supports_json=True)
	enginr_cc_o_p = Column(db.Integer, supports_dict=True, supports_json=True)
	enginr_cc_o_ac = Column(db.Integer, supports_dict=True, supports_json=True)
	enginr_cm_below = Column(db.Integer, supports_dict=True, supports_json=True)
	enginr_cm_tran = Column(db.Integer, supports_dict=True, supports_json=True)
	enginr_cm_on = Column(db.Integer, supports_dict=True, supports_json=True)
	enginr_cm_b_l = Column(db.Integer, supports_dict=True, supports_json=True)
	enginr_cm_b_p = Column(db.Integer, supports_dict=True, supports_json=True)
	enginr_cm_b_ac = Column(db.Integer, supports_dict=True, supports_json=True)
	enginr_cm_t_l = Column(db.Integer, supports_dict=True, supports_json=True)
	enginr_cm_t_p = Column(db.Integer, supports_dict=True, supports_json=True)
	enginr_cm_t_ac = Column(db.Integer, supports_dict=True, supports_json=True)
	enginr_cm_o_l = Column(db.Integer, supports_dict=True, supports_json=True)
	enginr_cm_o_p = Column(db.Integer, supports_dict=True, supports_json=True)
	enginr_cm_o_ac = Column(db.Integer, supports_dict=True, supports_json=True)
	natural = Column(db.Float(5), supports_dict=True, supports_json=True)
	natural_cc_below = Column(db.Integer, supports_dict=True, supports_json=True)
	natural_cc_tran = Column(db.Integer, supports_dict=True, supports_json=True)
	natural_cc_on = Column(db.Integer, supports_dict=True, supports_json=True)
	natural_cc_b_l = Column(db.Integer, supports_dict=True, supports_json=True)
	natural_cc_b_p = Column(db.Integer, supports_dict=True, supports_json=True)
	natural_cc_b_ac = Column(db.Integer, supports_dict=True, supports_json=True)
	natural_cc_t_l = Column(db.Integer, supports_dict=True, supports_json=True)
	natural_cc_t_p = Column(db.Integer, supports_dict=True, supports_json=True)
	natural_cc_t_ac = Column(db.Integer, supports_dict=True, supports_json=True)
	natural_cc_o_l = Column(db.Integer, supports_dict=True, supports_json=True)
	natural_cc_o_p = Column(db.Integer, supports_dict=True, supports_json=True)
	natural_cc_o_ac = Column(db.Integer, supports_dict=True, supports_json=True)
	natural_cm_below = Column(db.Integer, supports_dict=True, supports_json=True)
	natural_cm_tran = Column(db.Integer, supports_dict=True, supports_json=True)
	natural_cm_on = Column(db.Integer, supports_dict=True, supports_json=True)
	natural_cm_b_l = Column(db.Integer, supports_dict=True, supports_json=True)
	natural_cm_b_p = Column(db.Integer, supports_dict=True, supports_json=True)
	natural_cm_b_ac = Column(db.Integer, supports_dict=True, supports_json=True)
	natural_cm_t_l = Column(db.Integer, supports_dict=True, supports_json=True)
	natural_cm_t_p = Column(db.Integer, supports_dict=True, supports_json=True)
	natural_cm_t_ac = Column(db.Integer, supports_dict=True, supports_json=True)
	natural_cm_o_l = Column(db.Integer, supports_dict=True, supports_json=True)
	natural_cm_o_p = Column(db.Integer, supports_dict=True, supports_json=True)
	natural_cm_o_ac = Column(db.Integer, supports_dict=True, supports_json=True)

class DcCrawl(BaseModel):
	__tablename__ = 'dc_crawl'
	# Primary Key
	dc_crawl_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)
	
	# Foreign key
	ns_refuge_id = Column(db.Integer, db.ForeignKey('ns_refuge.ns_refuge_id'), nullable=False, supports_dict=True, supports_json=True)

	# Fields
	km = Column(db.Float(5), supports_dict=True, supports_json=True)
	type = Column(db.String(10), supports_dict=True, supports_json=True)

class Disorientation(BaseModel):
	__tablename__ = 'disorientation'
	# Primary Key
	disorientation_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)

	# Foreign key
	ns_refuge_id = Column(db.Integer, db.ForeignKey('ns_refuge.ns_refuge_id'), nullable=False, supports_dict=True, supports_json=True)

	# Fields
	km = Column(db.Float(5), supports_dict=True, supports_json=True)
	adult = Column(db.String(10), supports_dict=True, supports_json=True)
	hatchling = Column(db.String(10), supports_dict=True, supports_json=True)

class Depredation(BaseModel):
	__tablename__ = 'depredation'
	# Primary Key
	depredation_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)

	# Foreign key
	ns_refuge_id = Column(db.Integer, db.ForeignKey('ns_refuge.ns_refuge_id'), nullable=False, supports_dict=True, supports_json=True)

	# Fields
	species = Column(db.String(30), supports_dict=True, supports_json=True)
	km = Column(db.Float(5), supports_dict=True, supports_json=True)
	predator = Column(db.String(30), supports_dict=True, supports_json=True)
	eggs_destroyed = Column(db.Integer, supports_dict=True, supports_json=True)
	stake_number = Column(db.String(30), supports_dict=True, supports_json=True)

class TurtleSchema(ma.ModelSchema):
	class Meta:
		model = Turtle

class TagSchema(ma.ModelSchema):
	class Meta:
		model = Tag

class ClutchSchema(ma.ModelSchema):
	class Meta:
		model = Clutch

class MorphometricsSchema(ma.ModelSchema):
	class Meta:
		model = Morphometrics

class EncounterSchema(ma.ModelSchema):
	class Meta:
		model = Encounter

class SampleTrackingSchema(ma.ModelSchema):
	class Meta:
		model = SampleTracking

class SampleSchema(ma.ModelSchema):
	class Meta:
		model = Sample
	tracking_entries = ma.Nested(SampleTrackingSchema, many=True)

class TridentEncounterSchema(ma.ModelSchema):
	class Meta:
		model = TridentEncounter

class LagoonEncounterSchema(ma.ModelSchema):
	class Meta:
		model = LagoonEncounter

class BeachEncounterSchema(ma.ModelSchema):
	class Meta:
		model = BeachEncounter

class MetadataSchema(ma.ModelSchema):
	class Meta:
		model = Metadata

class NetSchema(ma.ModelSchema):
	class Meta:
		model = Net

class IncidentalCaptureSchema(ma.ModelSchema):
	class Meta:
		model = IncidentalCapture

class SampleHistorySchema(ma.Schema):
	class Meta:
		fields = ("sample_id", "tracking_entries")
	tracking_entries = ma.Nested(SampleTrackingSchema, many=True)

class NSRefugeSchema(ma.Schema):
	class Meta:
		model = NSRefuge

class DcCrawlSchema(ma.Schema):
	class Meta:
		model = DcCrawl

class DisorientationSchema(ma.Schema):
	class Meta:
		model = Disorientation

class DepredationSchema(ma.Schema):
	class Meta:
		model = Depredation

class TurtleQuerySchema(ma.Schema):
    species = fields.Str()

class EncounterQuerySchema(ma.Schema):
    encounter_id = fields.Int()
    turtle_id = fields.Int()
    encounter_date = fields.Date()
    type = fields.Str()
    entered_by = fields.Str()

class LagoonQuerySchema(ma.Schema):
    encounter_id = fields.Int()
    turtle_id = fields.Int()
    encounter_date = fields.Date()
    type = fields.Str()
    entered_by = fields.Str()
    species = fields.Pluck(TurtleSchema, 'species', attribute='turtle')
    metadata_location = fields.Pluck(MetadataSchema, 'metadata_location', attribute='metadata')

class FullLagoonQuerySchema(ma.Schema):	
	# def on_bind_field(self, field_name, field_obj):
	# # Override default missing attribute so
	# # that missing values deserialize to None
	# 	if field_obj.missing == missing:
	# 		field_obj.missing = None
	# 		field_obj.allow_none = True
	class Meta:
		additional = ('encounter_id', 'turtle_id','metadata_id','turtle_id','encounter_date','encounter_time','investigated_by','entered_by','entered_date','verified_by','verified_date','notes','paps_present','pap_category','paps_regression','photos','pap_photos','living_tags','other','leeches','leeches_where','leech_eggs','leech_eggs_where')
	
	species = fields.Pluck(TurtleSchema, 'species', attribute='turtle')
	samples = ma.Nested(SampleTrackingSchema)
	morphometrics = ma.Nested(MorphometricsSchema)
	nets = ma.Nested(NetSchema)
	incidentalcaptures = ma.Nested(IncidentalCaptureSchema)
	
	### None of these seem to include tags successfully:

	# tags = ma.Nested(TagSchema, attribute='turtle', supports_dict=True, supports_json=True) 
	# tags = fields.Nested(TagSchema, data_key='turtle_id', supports_dict=True, supports_json=True)
	# tags = fields.Nested(TagSchema, many=True, supports_dict=True, supports_json=True)
	# tags = fields.List(fields.Nested(TagSchema, many=True), supports_dict=True, supports_json=True) 

	# # Keys
	# encounter_id = fields.Int(, supports_dict=True, supports_json=True)
	# lagoon_encounter_id = fields.Int(, supports_dict=True, supports_json=True)
	# metadata_id = fields.Int(, supports_dict=True, supports_json=True)
	# turtle_id = fields.Int(, supports_dict=True, supports_json=True)

	# # # Dependencies
	# # samples = ma.Nested(SampleTrackingSchema, supports_dict=True, supports_json=True)
	# # morphometrics = ma.Nested(MorphometricsSchema, supports_dict=True, supports_json=True)

	# # # Fields common to all encounter types
	# # encounter_date = fields.Date(, supports_dict=True, supports_json=True)
	# # encounter_time = fields.Time(, supports_dict=True, supports_json=True)
	# # investigated_by = fields.Str(, supports_dict=True, supports_json=True)
	# # entered_by = fields.Str(, supports_dict=True, supports_json=True)
	# # entered_date = fields.Date(, supports_dict=True, supports_json=True)
	# # verified_by =  fields.Str(, supports_dict=True, supports_json=True)
	# # verified_date =  fields.Date(, supports_dict=True, supports_json=True)
	# # notes =  fields.Str(, supports_dict=True, supports_json=True)

	# # # Paps
	# # paps_present = fields.Boolean(, supports_dict=True, supports_json=True)
	# # pap_category = fields.Int(, supports_dict=True, supports_json=True)
	# # paps_regression = fields.Str(, supports_dict=True, supports_json=True)
	# # photos = fields.Boolean(, supports_dict=True, supports_json=True)
	# # pap_photos = fields.Boolean(, supports_dict=True, supports_json=True)

	# # # Fields unique to lagoon encounters
	# # living_tags = fields.Boolean(, supports_dict=True, supports_json=True)
	# # other = fields.Str(, supports_dict=True, supports_json=True)
	# # leeches = fields.Boolean(, supports_dict=True, supports_json=True)
	# # leeches_where = fields.Str(, supports_dict=True, supports_json=True)
	# # leech_eggs = fields.Boolean(, supports_dict=True, supports_json=True)
	# # leech_eggs_where = fields.Str(, supports_dict=True, supports_json=True)
