from turtleapi import db, ma
from flask import jsonify
from sqlathanor import declarative_base, Column, relationship
from datetime import datetime
from sqlalchemy.orm import backref

BaseModel = declarative_base()
#BaseModel = db.Model

def parse_time(value):
	if value is None:
		return None

	if isinstance(value, str):   					# strptime expects a str
		return datetime.strptime(value, '%H:%M')
	else:                        					# otherwise, try returning it. E.x. datetime, time, None
		return value.strftime('%H:%M')

def parse_date(value):
	if value is None:
		return None
		
	if isinstance(value, str):
		return datetime.strptime(value, '%Y-%m-%d')
	else:
		return value.strftime('%Y-%m-%d')

class Turtle(BaseModel):
	__tablename__ = 'turtle'
	# Primary key
	turtle_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)

	# Dependencies
	tags = relationship('Tag', backref='turtle', cascade="save-update, merge, delete", supports_dict=True, supports_json=True)
	encounters = relationship('Encounter', backref='turtle', cascade="save-update, merge, delete", lazy='dynamic', supports_dict=True, supports_json=True)	

	# Various fields
	species = Column(db.String(30), supports_dict=True, supports_json=True)
	sex = Column(db.Text, supports_dict=True, supports_json=True)
	old_turtle_id = Column(db.Integer, supports_dict=True, supports_json=True)

class Tag(BaseModel):
	__tablename__ = 'tag'
	# Primary key
	tag_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)
	
	# Foreign key
	turtle_id = Column(db.ForeignKey('turtle.turtle_id'), nullable=False, supports_dict=True, supports_json=True)

	# Various fields
	tag_number = Column(db.String(30), supports_dict=True, supports_json=True)
	active = Column(db.Boolean, supports_dict=True, supports_json=True)
	tag_type = Column(db.String(30), supports_dict=True, supports_json=True)
	pit = Column(db.Boolean, supports_dict=True, supports_json=True)

class Clutch(BaseModel):
	__tablename__ = 'clutch'
	# Primary key
	clutch_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)
	
	# Foreign key
	encounter_id = Column(db.Integer, db.ForeignKey('encounter.encounter_id'), nullable=False, supports_dict=True, supports_json=True)

	# Various fields
	stake_number = Column(db.String(30), supports_dict=True, supports_json=True)
	clutch_deposited = Column(db.Boolean, supports_dict=True, supports_json=True)
	sand_type = Column(db.String(50), supports_dict=True, supports_json=True)
	placement = Column(db.String(20), supports_dict=True, supports_json=True)
	emergence_date = Column(db.Date, supports_dict=True, supports_json=True, on_serialize=parse_date, on_deserialize=parse_date)
	inventory_date = Column(db.Date, supports_dict=True, supports_json=True, on_serialize=parse_date, on_deserialize=parse_date)
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
	entered_date = Column(db.Date, supports_dict=True, supports_json=True, on_serialize=parse_date, on_deserialize=parse_date)
	verified_by = Column(db.String(40), supports_dict=True, supports_json=True)
	verified_date = Column(db.Date, supports_dict=True, supports_json=True, on_serialize=parse_date, on_deserialize=parse_date)
	
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
	curved_length_over_barnacles = Column(db.Boolean, supports_dict=True, supports_json=True)
	straight_length = Column(db.Float(5), supports_dict=True, supports_json=True)
	minimum_length = Column(db.Float(5), supports_dict=True, supports_json=True)
	plastron_length = Column(db.Float(5), supports_dict=True, supports_json=True)
	plastron_length_over_barnacles = Column(db.Boolean, supports_dict=True, supports_json=True)
	weight = Column(db.Float(5), supports_dict=True, supports_json=True)
	curved_width = Column(db.Float(5), supports_dict=True, supports_json=True)
	curved_width_over_barnacles = Column(db.Boolean, supports_dict=True, supports_json=True)
	straight_width = Column(db.Float(5), supports_dict=True, supports_json=True)
	tail_length_pl_vent = Column(db.Float(5), supports_dict=True, supports_json=True)
	tail_length_pl_tip = Column(db.Float(5), supports_dict=True, supports_json=True)
	head_width = Column(db.Float(5), supports_dict=True, supports_json=True)
	body_depth = Column(db.Float(5), supports_dict=True, supports_json=True)
	body_depth_over_barnacles = Column(db.Boolean, supports_dict=True, supports_json=True)
	flipper_damage = Column(db.Text, supports_dict=True, supports_json=True)
	carapace_damage = Column(db.Text, supports_dict=True, supports_json=True)

class Metadata(BaseModel):
	__tablename__ = 'metadata'
	# Primary key
	metadata_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)

	# Dependencies
	encounters = relationship('Encounter', backref='metadata', supports_dict=True, supports_json=True)
	nets = relationship('Net', backref='metadata', cascade="save-update, merge, delete", lazy=True, supports_dict=True, supports_json=True)
	incidental_captures = relationship('IncidentalCapture', backref='metadata', cascade="save-update, merge, delete", supports_dict=True, supports_json=True)

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
	metadata_date = Column(db.Date, supports_dict=True, supports_json=True, on_serialize=parse_date, on_deserialize=parse_date)
	metadata_location = Column(db.Text, supports_dict=True, supports_json=True)
	metadata_investigators = Column(db.Text, supports_dict=True, supports_json=True)
	number_of_cc_captured = Column(db.Integer, supports_dict=True, supports_json=True)
	number_of_cm_captured = Column(db.Integer, supports_dict=True, supports_json=True)
	number_of_other_captured = Column(db.Integer, supports_dict=True, supports_json=True)

	# Environment
	water_sample = Column(db.Boolean, supports_dict=True, supports_json=True)
	wind_speed = Column(db.Float(5), supports_dict=True, supports_json=True)
	wind_dir = Column(db.String(20), supports_dict=True, supports_json=True)
	environment_time = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time, on_serialize=parse_time)
	weather = Column(db.Text, supports_dict=True, supports_json=True)
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
	metadata_date = Column(db.Date, supports_dict=True, supports_json=True, on_serialize=parse_date, on_deserialize=parse_date)
	metadata_location = Column(db.Text, supports_dict=True, supports_json=True)
	metadata_investigators = Column(db.Text, supports_dict=True, supports_json=True)
	number_of_cc_captured = Column(db.Integer, supports_dict=True, supports_json=True)
	number_of_cm_captured = Column(db.Integer, supports_dict=True, supports_json=True)
	number_of_other_captured = Column(db.Integer, supports_dict=True, supports_json=True)

	# Environment
	water_sample = Column(db.Boolean, supports_dict=True, supports_json=True)
	wind_speed = Column(db.Float(5), supports_dict=True, supports_json=True)
	wind_dir = Column(db.String(20), supports_dict=True, supports_json=True)
	environment_time = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time, on_serialize=parse_time)
	weather = Column(db.Text, supports_dict=True, supports_json=True)
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
	capture_date = Column(db.Date, supports_dict=True, supports_json=True, on_serialize=parse_date, on_deserialize=parse_date)
	capture_time = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time, on_serialize=parse_time)
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
	release_time = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time, on_serialize=parse_time)
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

class OtherMetadata(Metadata):
	__tablename__ = 'other_metadata'
	# Foreign key
	metadata_id = Column(db.Integer, db.ForeignKey('metadata.metadata_id'), primary_key=True, nullable=False, supports_dict=True, supports_json=True)

	# Various fields
	metadata_date = Column(db.Date, supports_dict=True, supports_json=True, on_serialize=parse_date, on_deserialize=parse_date)
	environment_time = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time, on_serialize=parse_time)
	weather = Column(db.Text, supports_dict=True, supports_json=True)
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
		'polymorphic_identity': 'other'
	}

class Encounter(BaseModel):
	__tablename__ = 'encounter'
	# Primary key
	encounter_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)

	# Foreign keys
	metadata_id = Column(db.Integer, db.ForeignKey('metadata.metadata_id'))
	turtle_id = Column(db.Integer, db.ForeignKey('turtle.turtle_id'), nullable=False, supports_dict=True, supports_json=True)

	# Dependencies
	samples = relationship('Sample', backref='encounter', cascade="save-update, merge, delete", supports_dict=True, supports_json=True)
	morphometrics = relationship('Morphometrics', backref=backref('encounter', uselist=False), cascade="save-update, merge, delete", supports_dict=True, supports_json=True)
	clutches = relationship('Clutch', backref=backref('encounter', uselist=False), cascade="save-update, merge, delete", supports_dict=True, supports_json=True)

	# Fields
	old_encounter_id = Column(db.Integer, supports_dict=True, supports_json=True)
	pdf_filename = Column(db.Text, unique=True, supports_dict=True, supports_json=True)
	img_filename = Column(db.Text, unique=True, supports_dict=True, supports_json=True)

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
	tracking_entries = relationship('SampleTracking', backref='sample', cascade="save-update, merge, delete", lazy='joined', supports_dict=True, supports_json=True)

	# Various fields
	sample_type = Column(db.Text, supports_dict=True, supports_json=True)
	received_by = Column(db.Text, supports_dict=True, supports_json=True)
	purpose_of_sample = Column(db.Text, supports_dict=True, supports_json=True)
	notes = Column(db.Text, supports_dict=True, supports_json=True)
	entered_date = Column(db.Date, supports_dict=True, supports_json=True, on_serialize=parse_date, on_deserialize=parse_date)
	entered_by = Column(db.Text, supports_dict=True, supports_json=True)

class TridentEncounter(Encounter):
	__tablename__ = 'trident_encounter'
	# Primary key
	encounter_id = Column(db.Integer, db.ForeignKey('encounter.encounter_id'), primary_key=True, nullable=False, supports_dict=True, supports_json=True)
	
	# Fields common to all encounter types
	encounter_date = Column(db.Date, supports_dict=True, supports_json=True, on_serialize=parse_date, on_deserialize=parse_date)
	encounter_time = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time, on_serialize=parse_time)
	capture_type = Column(db.String(40), supports_dict=True, supports_json=True)
	investigated_by = Column(db.String(500), supports_dict=True, supports_json=True)
	entered_by = Column(db.String(30), supports_dict=True, supports_json=True)
	entered_date = Column(db.Date, supports_dict=True, supports_json=True, on_serialize=parse_date, on_deserialize=parse_date)
	verified_by = Column(db.String(30), supports_dict=True, supports_json=True)
	verified_date = Column(db.Date, supports_dict=True, supports_json=True, on_serialize=parse_date, on_deserialize=parse_date)
	notes = Column(db.Text, supports_dict=True, supports_json=True)
	scanned = Column(db.Boolean, supports_dict=True, supports_json=True)
	tag_scars = Column(db.String(20), supports_dict=True, supports_json=True)
	tag1 = Column(db.String(30), supports_dict=True, supports_json=True)
	tag2 = Column(db.String(30), supports_dict=True, supports_json=True)
	tag3 = Column(db.String(30), supports_dict=True, supports_json=True)

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
	encounter_date = Column(db.Date, supports_dict=True, supports_json=True, on_serialize=parse_date, on_deserialize=parse_date)
	encounter_time = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time, on_serialize=parse_time)
	capture_type = Column(db.String(40), supports_dict=True, supports_json=True)
	investigated_by = Column(db.String(500), supports_dict=True, supports_json=True)
	entered_by = Column(db.String(30), supports_dict=True, supports_json=True)
	entered_date = Column(db.Date, supports_dict=True, supports_json=True, on_serialize=parse_date, on_deserialize=parse_date)
	verified_by = Column(db.String(30), supports_dict=True, supports_json=True)
	verified_date = Column(db.Date, supports_dict=True, supports_json=True, on_serialize=parse_date, on_deserialize=parse_date)
	notes = Column(db.Text, supports_dict=True, supports_json=True)
	scanned = Column(db.Boolean, supports_dict=True, supports_json=True)
	tag_scars = Column(db.String(20), supports_dict=True, supports_json=True)
	tag1 = Column(db.String(30), supports_dict=True, supports_json=True)
	tag2 = Column(db.String(30), supports_dict=True, supports_json=True)
	tag3 = Column(db.String(30), supports_dict=True, supports_json=True)

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
	encounter_date = Column(db.Date, supports_dict=True, supports_json=True, on_serialize=parse_date, on_deserialize=parse_date)
	encounter_time = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time, on_serialize=parse_time)
	capture_type = Column(db.String(40), supports_dict=True, supports_json=True)
	investigated_by = Column(db.String(500), supports_dict=True, supports_json=True)
	entered_by = Column(db.String(30), supports_dict=True, supports_json=True)
	entered_date = Column(db.Date, supports_dict=True, supports_json=True, on_serialize=parse_date, on_deserialize=parse_date)
	verified_by = Column(db.String(30), supports_dict=True, supports_json=True)
	verified_date = Column(db.Date, supports_dict=True, supports_json=True, on_serialize=parse_date, on_deserialize=parse_date)
	scanned = Column(db.Boolean, supports_dict=True, supports_json=True)
	tag_scars = Column(db.String(20), supports_dict=True, supports_json=True)
	scanner_number = Column(db.String(30), supports_dict=True, supports_json=True)
	tag1 = Column(db.String(30), supports_dict=True, supports_json=True)
	tag2 = Column(db.String(30), supports_dict=True, supports_json=True)
	tag3 = Column(db.String(30), supports_dict=True, supports_json=True)

	# Fields unique to beach encounters
	prime_tag = Column(db.String(30), supports_dict=True, supports_json=True)
	days_45 = Column(db.Date, supports_dict=True, supports_json=True, on_serialize=parse_date, on_deserialize=parse_date)
	days_70 = Column(db.Date, supports_dict=True, supports_json=True, on_serialize=parse_date, on_deserialize=parse_date)
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
	can_buried = Column(db.String(10), supports_dict=True, supports_json=True)
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

class OffshoreEncounter(Encounter):
	__tablename__ = 'offshore_encounter'
	# Primary key
	encounter_id = Column(db.Integer, db.ForeignKey('encounter.encounter_id'), primary_key=True, nullable=False, supports_dict=True, supports_json=True)

	# Fields unique to offshore encounters
	trip_number = Column(db.Text, supports_dict=True, supports_json=True)
	capture_habitat = Column(db.Text, supports_dict=True, supports_json=True)
	notes = Column(db.Text, supports_dict=True, supports_json=True)
	scanned = Column(db.Boolean, supports_dict=True, supports_json=True)
	magnet_off = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time, on_serialize=parse_time)
	tag1 = Column(db.String(30), supports_dict=True, supports_json=True)
	tag2 = Column(db.String(30), supports_dict=True, supports_json=True)
	scanner_number = Column(db.Text, supports_dict=True, supports_json=True)
	entered_by = Column(db.Date, supports_dict=True, supports_json=True, on_deserialize=parse_date, on_serialize=parse_date)
	entered_by = Column(db.String(30), supports_dict=True, supports_json=True)

	# Polymorphism
	__mapper_args__ = {
		'polymorphic_identity': 'offshore'
	}

class OtherEncounter(Encounter):
	__tablename__ = 'other_encounter'
	# Primary key
	encounter_id = Column(db.Integer, db.ForeignKey('encounter.encounter_id'), primary_key=True, nullable=False, supports_dict=True, supports_json=True)

	# Fields unique to other encounters
	name = Column(db.String(30), supports_dict=True, supports_json=True)
	encounter_date = Column(db.Date, supports_dict=True, supports_json=True, on_serialize=parse_date, on_deserialize=parse_date)
	encounter_time = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time, on_serialize=parse_time)
	investigated_by = Column(db.String(500), supports_dict=True, supports_json=True)
	notes = Column(db.Text, supports_dict=True, supports_json=True)
	paps_present = Column(db.Boolean, supports_dict=True, supports_json=True)
	pap_category = Column(db.Integer, supports_dict=True, supports_json=True)
	paps_regressed = Column(db.String(40), supports_dict=True, supports_json=True)
	pap_photo = Column(db.Boolean, supports_dict=True, supports_json=True)
	leeches = Column(db.Boolean, supports_dict=True, supports_json=True)
	leeches_where = Column(db.Text, supports_dict=True, supports_json=True)
	leech_eggs = Column(db.Boolean, supports_dict=True, supports_json=True)

	# Polymorphism
	__mapper_args__ = {
		'polymorphic_identity': 'other'
	}

class Net(BaseModel):
	__tablename__ = 'net'
	# Primary key
	net_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)
	
	# Foreign key
	metadata_id = Column(db.Integer, db.ForeignKey('metadata.metadata_id'), nullable=False, supports_dict=True, supports_json=True)

	# Various fields
	net_deploy_start_time = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time, on_serialize=parse_time)
	net_deploy_end_time = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time, on_serialize=parse_time)
	net_retrieval_start_time = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time, on_serialize=parse_time)
	net_retrieval_end_time = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time, on_serialize=parse_time)
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
	capture_time = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time, on_serialize=parse_time)
	measurement = Column(db.Text, supports_dict=True, supports_json=True)
	notes = Column(db.Text, supports_dict=True, supports_json=True)

class SampleTracking(BaseModel):
	__tablename__ = 'sample_tracking'
	# Primary key
	sample_tracking_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)

	# Foreign key
	sample_id = Column(db.Integer, db.ForeignKey('sample.sample_id'), nullable=False, supports_dict=True, supports_json=True)

	# Fields
	date = Column(db.Date, supports_dict=True, supports_json=True, on_serialize=parse_date, on_deserialize=parse_date)
	notes = Column(db.Text, supports_dict=True, supports_json=True)

class NSRefuge(BaseModel):
	__tablename__ = 'ns_refuge'
	# Primary key
	ns_refuge_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)

	# Fields
	type = Column(db.String(1), supports_dict=True, supports_json=True)
	date = Column(db.Date, supports_dict=True, supports_json=True, on_serialize=parse_date, on_deserialize=parse_date)
	initials = Column(db.String(30), supports_dict=True, supports_json=True)
	notes = Column(db.Text, supports_dict=True, supports_json=True)

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
	enginr_cc_before = Column(db.Integer, supports_dict=True, supports_json=True)
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
	enginr_cm_before = Column(db.Integer, supports_dict=True, supports_json=True)
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
	natural_cc_before = Column(db.Integer, supports_dict=True, supports_json=True)
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
	natural_cm_before = Column(db.Integer, supports_dict=True, supports_json=True)
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

class BigSurvey(BaseModel):
	__tablename__ = 'big_survey'
	# Primary key
	big_survey_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)

	# Dependencies
	emergences = relationship('Emergence', backref='big_survey', cascade="save-update, merge, delete", supports_dict=True, supports_json=True)
	
	# Fields
	type = Column(db.String(30), supports_dict=True, supports_json=True) # PAFB / mid / south
	date = Column(db.Date, supports_dict=True, supports_json=True, on_serialize=parse_date, on_deserialize=parse_date)
	initials = Column(db.String(30), supports_dict=True, supports_json=True)
	notes = Column(db.Text, supports_dict=True, supports_json=True)

	# Below HTL
	below_htl_cc_nest = Column(db.Integer, supports_dict=True, supports_json=True)
	below_htl_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	below_htl_cm_nest = Column(db.Integer, supports_dict=True, supports_json=True)
	below_htl_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	below_htl_dc_nest = Column(db.Integer, supports_dict=True, supports_json=True)
	below_htl_dc_fc = Column(db.Integer, supports_dict=True, supports_json=True)

	# Nest Fields
	km_25_45s_0_b_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_25_45s_0_t_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_25_45s_0_o_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_25_45s_0_b_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_25_45s_0_t_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_25_45s_0_o_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_3_4s_05_b_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_3_4s_05_t_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_3_4s_05_o_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_3_4s_05_b_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_3_4s_05_t_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_3_4s_05_o_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_35_35s_1_b_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_35_35s_1_t_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_35_35s_1_o_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_35_35s_1_b_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_35_35s_1_t_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_35_35s_1_o_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_4_3s_15_b_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_4_3s_15_t_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_4_3s_15_o_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_4_3s_15_b_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_4_3s_15_t_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_4_3s_15_o_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_45_25s_2_b_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_45_25s_2_t_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_45_25s_2_o_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_45_25s_2_b_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_45_25s_2_t_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_45_25s_2_o_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_5_2s_25_b_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_5_2s_25_t_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_5_2s_25_o_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_5_2s_25_b_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_5_2s_25_t_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_5_2s_25_o_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_55_15s_3_b_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_55_15s_3_t_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_55_15s_3_o_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_55_15s_3_b_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_55_15s_3_t_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_55_15s_3_o_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_6_1s_35_b_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_6_1s_35_t_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_6_1s_35_o_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_6_1s_35_b_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_6_1s_35_t_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_6_1s_35_o_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_65_05s_4_b_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_65_05s_4_t_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_65_05s_4_o_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_65_05s_4_b_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_65_05s_4_t_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_65_05s_4_o_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_7_0s_45_b_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_7_0s_45_t_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_7_0s_45_o_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_7_0s_45_b_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_7_0s_45_t_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_7_0s_45_o_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_75_0n_5_b_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_75_0n_5_t_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_75_0n_5_o_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_75_0n_5_b_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_75_0n_5_t_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_75_0n_5_o_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_8_05n_55_b_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_8_05n_55_t_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_8_05n_55_o_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_8_05n_55_b_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_8_05n_55_t_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_8_05n_55_o_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_85_1n_6_b_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_85_1n_6_t_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_85_1n_6_o_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_85_1n_6_b_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_85_1n_6_t_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_85_1n_6_o_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_9_15n_65_b_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_9_15n_65_t_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_9_15n_65_o_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_9_15n_65_b_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_9_15n_65_t_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_9_15n_65_o_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_95_2n_b_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_95_2n_t_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_95_2n_o_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_95_2n_b_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_95_2n_t_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_95_2n_o_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_10_b_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_10_t_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_10_o_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_10_b_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_10_t_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_10_o_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_105_b_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_105_t_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_105_o_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_105_b_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_105_t_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_105_o_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_11_b_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_11_t_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_11_o_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_11_b_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_11_t_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_11_o_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_115_b_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_115_t_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_115_o_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_115_b_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_115_t_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_115_o_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_12_b_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_12_t_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_12_o_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_12_b_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_12_t_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_12_o_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_125_b_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_125_t_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_125_o_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_125_b_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_125_t_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_125_o_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_13_b_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_13_t_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_13_o_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_13_b_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_13_t_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_13_o_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_135_b_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_135_t_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_135_o_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_135_b_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_135_t_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_135_o_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_14_b_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_14_t_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_14_o_cc_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_14_b_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_14_t_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)
	km_14_o_cm_nests = Column(db.Integer, supports_dict=True, supports_json=True)

	# False Crawls Fields
	km_25_45s_0_before_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_25_45s_0_before_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_25_45s_0_before_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_25_45s_0_before_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_25_45s_0_before_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_25_45s_0_before_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_25_45s_0_tran_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_25_45s_0_tran_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_25_45s_0_tran_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_25_45s_0_tran_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_25_45s_0_tran_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_25_45s_0_tran_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_25_45s_0_on_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_25_45s_0_on_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_25_45s_0_on_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_25_45s_0_on_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_25_45s_0_on_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_25_45s_0_on_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_3_4s_05_before_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_3_4s_05_before_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_3_4s_05_before_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_3_4s_05_before_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_3_4s_05_before_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_3_4s_05_before_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_3_4s_05_tran_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_3_4s_05_tran_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_3_4s_05_tran_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_3_4s_05_tran_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_3_4s_05_tran_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_3_4s_05_tran_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_3_4s_05_on_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_3_4s_05_on_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_3_4s_05_on_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_3_4s_05_on_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_3_4s_05_on_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_3_4s_05_on_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_35_35s_1_before_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_35_35s_1_before_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_35_35s_1_before_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_35_35s_1_before_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_35_35s_1_before_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_35_35s_1_before_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_35_35s_1_tran_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_35_35s_1_tran_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_35_35s_1_tran_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_35_35s_1_tran_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_35_35s_1_tran_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_35_35s_1_tran_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_35_35s_1_on_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_35_35s_1_on_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_35_35s_1_on_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_35_35s_1_on_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_35_35s_1_on_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_35_35s_1_on_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_4_3s_15_before_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_4_3s_15_before_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_4_3s_15_before_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_4_3s_15_before_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_4_3s_15_before_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_4_3s_15_before_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_4_3s_15_tran_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_4_3s_15_tran_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_4_3s_15_tran_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_4_3s_15_tran_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_4_3s_15_tran_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_4_3s_15_tran_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_4_3s_15_on_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_4_3s_15_on_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_4_3s_15_on_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_4_3s_15_on_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_4_3s_15_on_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_4_3s_15_on_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_45_25s_2_before_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_45_25s_2_before_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_45_25s_2_before_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_45_25s_2_before_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_45_25s_2_before_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_45_25s_2_before_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_45_25s_2_tran_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_45_25s_2_tran_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_45_25s_2_tran_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_45_25s_2_tran_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_45_25s_2_tran_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_45_25s_2_tran_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_45_25s_2_on_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_45_25s_2_on_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_45_25s_2_on_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_45_25s_2_on_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_45_25s_2_on_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_45_25s_2_on_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_5_2s_25_before_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_5_2s_25_before_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_5_2s_25_before_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_5_2s_25_before_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_5_2s_25_before_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_5_2s_25_before_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_5_2s_25_tran_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_5_2s_25_tran_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_5_2s_25_tran_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_5_2s_25_tran_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_5_2s_25_tran_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_5_2s_25_tran_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_5_2s_25_on_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_5_2s_25_on_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_5_2s_25_on_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_5_2s_25_on_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_5_2s_25_on_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_5_2s_25_on_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_55_15s_3_before_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_55_15s_3_before_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_55_15s_3_before_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_55_15s_3_before_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_55_15s_3_before_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_55_15s_3_before_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_55_15s_3_tran_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_55_15s_3_tran_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_55_15s_3_tran_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_55_15s_3_tran_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_55_15s_3_tran_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_55_15s_3_tran_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_55_15s_3_on_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_55_15s_3_on_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_55_15s_3_on_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_55_15s_3_on_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_55_15s_3_on_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_55_15s_3_on_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_6_1s_35_before_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_6_1s_35_before_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_6_1s_35_before_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_6_1s_35_before_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_6_1s_35_before_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_6_1s_35_before_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_6_1s_35_tran_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_6_1s_35_tran_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_6_1s_35_tran_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_6_1s_35_tran_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_6_1s_35_tran_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_6_1s_35_tran_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_6_1s_35_on_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_6_1s_35_on_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_6_1s_35_on_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_6_1s_35_on_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_6_1s_35_on_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_6_1s_35_on_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_65_05s_4_before_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_65_05s_4_before_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_65_05s_4_before_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_65_05s_4_before_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_65_05s_4_before_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_65_05s_4_before_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_65_05s_4_tran_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_65_05s_4_tran_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_65_05s_4_tran_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_65_05s_4_tran_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_65_05s_4_tran_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_65_05s_4_tran_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_65_05s_4_on_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_65_05s_4_on_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_65_05s_4_on_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_65_05s_4_on_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_65_05s_4_on_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_65_05s_4_on_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_7_0s_45_before_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_7_0s_45_before_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_7_0s_45_before_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_7_0s_45_before_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_7_0s_45_before_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_7_0s_45_before_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_7_0s_45_tran_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_7_0s_45_tran_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_7_0s_45_tran_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_7_0s_45_tran_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_7_0s_45_tran_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_7_0s_45_tran_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_7_0s_45_on_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_7_0s_45_on_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_7_0s_45_on_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_7_0s_45_on_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_7_0s_45_on_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_7_0s_45_on_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_75_0n_5_before_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_75_0n_5_before_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_75_0n_5_before_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_75_0n_5_before_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_75_0n_5_before_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_75_0n_5_before_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_75_0n_5_tran_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_75_0n_5_tran_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_75_0n_5_tran_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_75_0n_5_tran_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_75_0n_5_tran_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_75_0n_5_tran_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_75_0n_5_on_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_75_0n_5_on_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_75_0n_5_on_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_75_0n_5_on_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_75_0n_5_on_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_75_0n_5_on_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_8_05n_55_before_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_8_05n_55_before_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_8_05n_55_before_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_8_05n_55_before_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_8_05n_55_before_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_8_05n_55_before_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_8_05n_55_tran_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_8_05n_55_tran_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_8_05n_55_tran_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_8_05n_55_tran_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_8_05n_55_tran_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_8_05n_55_tran_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_8_05n_55_on_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_8_05n_55_on_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_8_05n_55_on_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_8_05n_55_on_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_8_05n_55_on_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_8_05n_55_on_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_85_1n_6_before_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_85_1n_6_before_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_85_1n_6_before_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_85_1n_6_before_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_85_1n_6_before_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_85_1n_6_before_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_85_1n_6_tran_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_85_1n_6_tran_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_85_1n_6_tran_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_85_1n_6_tran_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_85_1n_6_tran_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_85_1n_6_tran_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_85_1n_6_on_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_85_1n_6_on_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_85_1n_6_on_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_85_1n_6_on_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_85_1n_6_on_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_85_1n_6_on_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_9_15n_65_before_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_9_15n_65_before_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_9_15n_65_before_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_9_15n_65_before_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_9_15n_65_before_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_9_15n_65_before_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_9_15n_65_tran_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_9_15n_65_tran_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_9_15n_65_tran_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_9_15n_65_tran_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_9_15n_65_tran_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_9_15n_65_tran_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_9_15n_65_on_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_9_15n_65_on_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_9_15n_65_on_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_9_15n_65_on_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_9_15n_65_on_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_9_15n_65_on_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_95_2n_before_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_95_2n_before_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_95_2n_before_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_95_2n_before_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_95_2n_before_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_95_2n_before_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_95_2n_tran_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_95_2n_tran_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_95_2n_tran_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_95_2n_tran_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_95_2n_tran_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_95_2n_tran_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_95_2n_on_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_95_2n_on_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_95_2n_on_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_95_2n_on_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_95_2n_on_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_95_2n_on_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_10_before_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_10_before_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_10_before_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_10_before_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_10_before_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_10_before_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_10_tran_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_10_tran_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_10_tran_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_10_tran_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_10_tran_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_10_tran_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_10_on_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_10_on_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_10_on_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_10_on_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_10_on_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_10_on_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_105_before_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_105_before_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_105_before_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_105_before_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_105_before_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_105_before_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_105_tran_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_105_tran_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_105_tran_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_105_tran_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_105_tran_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_105_tran_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_105_on_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_105_on_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_105_on_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_105_on_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_105_on_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_105_on_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_11_before_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_11_before_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_11_before_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_11_before_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_11_before_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_11_before_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_11_tran_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_11_tran_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_11_tran_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_11_tran_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_11_tran_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_11_tran_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_11_on_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_11_on_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_11_on_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_11_on_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_11_on_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_11_on_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_115_before_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_115_before_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_115_before_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_115_before_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_115_before_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_115_before_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_115_tran_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_115_tran_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_115_tran_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_115_tran_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_115_tran_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_115_tran_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_115_on_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_115_on_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_115_on_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_115_on_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_115_on_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_115_on_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_12_before_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_12_before_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_12_before_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_12_before_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_12_before_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_12_before_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_12_tran_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_12_tran_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_12_tran_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_12_tran_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_12_tran_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_12_tran_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_12_on_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_12_on_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_12_on_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_12_on_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_12_on_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_12_on_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_125_before_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_125_before_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_125_before_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_125_before_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_125_before_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_125_before_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_125_tran_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_125_tran_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_125_tran_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_125_tran_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_125_tran_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_125_tran_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_125_on_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_125_on_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_125_on_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_125_on_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_125_on_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_125_on_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_13_before_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_13_before_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_13_before_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_13_before_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_13_before_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_13_before_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_13_tran_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_13_tran_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_13_tran_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_13_tran_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_13_tran_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_13_tran_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_13_on_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_13_on_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_13_on_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_13_on_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_13_on_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_13_on_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_135_before_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_135_before_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_135_before_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_135_before_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_135_before_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_135_before_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_135_tran_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_135_tran_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_135_tran_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_135_tran_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_135_tran_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_135_tran_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_135_on_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_135_on_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_135_on_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_135_on_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_135_on_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_135_on_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_14_before_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_14_before_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_14_before_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_14_before_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_14_before_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_14_before_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_14_tran_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_14_tran_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_14_tran_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_14_tran_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_14_tran_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_14_tran_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_14_on_l_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_14_on_l_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_14_on_p_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_14_on_p_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_14_on_a_cc_fc = Column(db.Integer, supports_dict=True, supports_json=True)
	km_14_on_a_cm_fc = Column(db.Integer, supports_dict=True, supports_json=True)

class DcCrawl(BaseModel):
	__tablename__ = 'dc_crawl'
	# Primary Key
	dc_crawl_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)

	# Fields
	km = Column(db.Float(5), supports_dict=True, supports_json=True)
	type = Column(db.String(10), supports_dict=True, supports_json=True)

class FalseCrawl(BaseModel):
	__tablename__ = 'false_crawl'
	# Primary Key
	false_crawl_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)

	# Fields
	date = Column(db.Date, supports_dict=True, supports_json=True, on_serialize=parse_date, on_deserialize=parse_date)
	species = Column(db.String(30), supports_dict=True, supports_json=True)
	project_area = Column(db.Boolean, supports_dict=True, supports_json=True)
	hit_scarp_over_18 = Column(db.Boolean, supports_dict=True, supports_json=True)
	type = Column(db.String(10), supports_dict=True, supports_json=True)
	distance_to_dune = Column(db.Float(5), supports_dict=True, supports_json=True)
	distance_to_high_tide = Column(db.Float(5), supports_dict=True, supports_json=True)
	location = Column(db.Float(5), supports_dict=True, supports_json=True)
	latitude = Column(db.Float(5), supports_dict=True, supports_json=True)
	longitude = Column(db.Float(5), supports_dict=True, supports_json=True)

class Scarp(BaseModel):
	__tablename__ = 'scarp'
	# Primary Key
	scarp_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)

	# Fields
	date = Column(db.Date, supports_dict=True, supports_json=True, on_serialize=parse_date, on_deserialize=parse_date)
	beginning_location = Column(db.Float(5), supports_dict=True, supports_json=True)
	end_location = Column(db.Float(5), supports_dict=True, supports_json=True)
	location = Column(db.String(15), supports_dict=True, supports_json=True)
	ns = Column(db.String(1), supports_dict=True, supports_json=True)
	height_of_scarp = Column(db.String(3), supports_dict=True, supports_json=True)
	length_of_scarp = Column(db.Integer, supports_dict=True, supports_json=True)
	placement = Column(db.String(15), supports_dict=True, supports_json=True)

class Disorientation(BaseModel):
	__tablename__ = 'disorientation'
	# Primary Key
	disorientation_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)

	# Fields
	km = Column(db.Float(5), supports_dict=True, supports_json=True)
	adult = Column(db.Integer, supports_dict=True, supports_json=True)
	hatchling = Column(db.Integer, supports_dict=True, supports_json=True)

class Depredation(BaseModel):
	__tablename__ = 'depredation'
	# Primary Key
	depredation_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)

	# Fields
	date = Column(db.Date, supports_dict=True, supports_json=True, on_serialize=parse_date, on_deserialize=parse_date)
	species = Column(db.String(30), supports_dict=True, supports_json=True)
	location = Column(db.Float(5), supports_dict=True, supports_json=True)
	ns = Column(db.String(1), supports_dict=True, supports_json=True)
	predator = Column(db.String(30), supports_dict=True, supports_json=True)
	eggs_destroyed = Column(db.Integer, supports_dict=True, supports_json=True)
	marked_nest_number = Column(db.String(30), supports_dict=True, supports_json=True)
	notes = Column(db.Text, supports_dict=True, supports_json=True)

class Emergence(BaseModel):
	__tablename__ = 'emergence'
	# Primary Key
	emergence_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)

	# Foreign keys
	big_survey_id = Column(db.Integer, db.ForeignKey('big_survey.big_survey_id'), nullable=False, supports_dict=True, supports_json=True)

	# Fields
	stake_number_1 = Column(db.String(30), supports_dict=True, supports_json=True)
	stake_number_2 = Column(db.String(30), supports_dict=True, supports_json=True)

class FilterSet(BaseModel):
	__tablename__ = 'filter_set'
	# Primary Key
	filter_set_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)

	# Fields
	username = Column(db.String(50), supports_dict=True, supports_json=True)
	filter_set_name = Column(db.String(50), supports_dict=True, supports_json=True)
	filter_data = Column(db.Text, supports_dict=True, supports_json=True)
	survey_filter_set = Column(db.String(1), supports_dict=True, supports_json=True)

class Legacy(BaseModel):
	__tablename__ = 'legacy'
	# Primary Key
	legacy_id = Column(db.Integer, primary_key=True, supports_dict=True, supports_json=True)

	# Foreign Key
	encounter_id = Column(db.Integer, db.ForeignKey('encounter.encounter_id'), nullable=False, supports_dict=True, supports_json=True)

	# Fields
	recapture_linear_dates = Column(db.Text, supports_dict=True, supports_json=True)
	pap_mapped = Column(db.Boolean, supports_dict=True, supports_json=True)
	papilloma_description = Column(db.Text, supports_dict=True, supports_json=True)
	disposal_of_specimen = Column(db.Text, supports_dict=True, supports_json=True)
	stake_summary = Column(db.Text, supports_dict=True, supports_json=True)
	survery_full_location = Column(db.Float(5), supports_dict=True, supports_json=True)
	clutch_moved = Column(db.Text, supports_dict=True, supports_json=True)
	clutch_fate = Column(db.Text, supports_dict=True, supports_json=True)
	eggs_yolked = Column(db.Integer, supports_dict=True, supports_json=True) 
	eggs_broken = Column(db.Integer, supports_dict=True, supports_json=True)
	eggs_yolkless = Column(db.Integer, supports_dict=True, supports_json=True)
	eggs_research = Column(db.Integer, supports_dict=True, supports_json=True)
	in_place_foil = Column(db.Boolean, supports_dict=True, supports_json=True)
	in_place_metal = Column(db.Boolean, supports_dict=True, supports_json=True)
	carap_l_greatest = Column(db.Float(5), supports_dict=True, supports_json=True)
	cloaca_temp = Column(db.Float(5), supports_dict=True, supports_json=True)
	interanal_scute = Column(db.Text, supports_dict=True, supports_json=True)
	date_laid = Column(db.Date, supports_dict=True, supports_json=True, on_serialize=parse_date, on_deserialize=parse_date)
	c1_embryo = Column(db.Integer, supports_dict=True, supports_json=True)
	c2_fetus = Column(db.Integer, supports_dict=True, supports_json=True)
	c6_infertile_eggs = Column(db.Integer, supports_dict=True, supports_json=True)
	d1_research = Column(db.Integer, supports_dict=True, supports_json=True)
	d2_poached = Column(db.Integer, supports_dict=True, supports_json=True)
	e2_washout = Column(db.Integer, supports_dict=True, supports_json=True)
	e3_inundated = Column(db.Integer, supports_dict=True, supports_json=True)
	d_nest_disturbed_summary = Column(db.Text, supports_dict=True, supports_json=True)
	nest_data_collection_problems = Column(db.Text, supports_dict=True, supports_json=True)
	wind_speed_min_mph = Column(db.Float(5), supports_dict=True, supports_json=True)
	wind_speed_max_mph = Column(db.Float(5), supports_dict=True, supports_json=True)
	wind_speed_min_mps = Column(db.Float(5), supports_dict=True, supports_json=True)
	wind_speed_max_mps = Column(db.Float(5), supports_dict=True, supports_json=True)
	depth = Column(db.Float(5), supports_dict=True, supports_json=True)
	length_units = Column(db.Text, supports_dict=True, supports_json=True)
	water_temp_3 = Column(db.Float(5), supports_dict=True, supports_json=True)
	salinity_3 = Column(db.Float(5), supports_dict=True, supports_json=True)
	secchi_depth = Column(db.Float(5), supports_dict=True, supports_json=True)
	secchi_distance_from_shore = Column(db.Float(5), supports_dict=True, supports_json=True)
	time_text_high_tide = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time, on_serialize=parse_time)
	time_text_low_tide = Column(db.Time, supports_dict=True, supports_json=True, on_deserialize=parse_time, on_serialize=parse_time)
	notes_environment = Column(db.Text, supports_dict=True, supports_json=True)
	clutch_other_egg_affected = Column(db.Integer, supports_dict=True, supports_json=True)
	
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
