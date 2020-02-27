from turtleapi import db, ma
from flask import jsonify
from marshmallow import Schema, fields, pre_dump, post_dump

class Turtle(db.Model):
	# Primary key
	turtle_id = db.Column(db.Integer, primary_key=True)

	# Dependencies
	tags = db.relationship('Tag', backref='turtle')
	clutches = db.relationship('Clutch', backref='turtle')
	morphometrics = db.relationship('Morphometrics', backref='turtle')
	encounters = db.relationship('Encounter', backref='turtle', lazy='dynamic')	

	# Various fields
	species = db.Column(db.String(30))
	old_turtle_id = db.Column(db.Integer)

class Tag(db.Model):
	# Primary key
	tag_id = db.Column(db.Integer, primary_key=True)
	
	# Foreign key
	turtle_id = db.Column(db.ForeignKey('turtle.turtle_id'), nullable=False)

	# Various fields
	tag_number = db.Column(db.String(30))
	tag_scars = db.Column(db.Boolean)
	active = db.Column(db.Boolean)
	tag_type = db.Column(db.String(30))
	pit = db.Column(db.Boolean)
	scanned = db.Column(db.Boolean)
	scanner_number = db.Column(db.String(30))

class Clutch(db.Model):
	# Primary key
	clutch_id = db.Column(db.Integer, primary_key=True)
	
	# Foreign key
	turtle_id = db.Column(db.Integer, db.ForeignKey('turtle.turtle_id'), nullable=False)

	# Various fields
	stake_number = db.Column(db.String(30))
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
	inventoried_by = db.Column(db.String(500))
	entered_by = db.Column(db.String(40))
	entered_date = db.Column(db.Date)
	verified_by = db.Column(db.String(40))
	verified_date = db.Column(db.Date)
	
	# Hatchlings
	hatched = db.Column(db.Integer)
	live_hatchlings = db.Column(db.Integer)
	dead_hatchlings = db.Column(db.Integer)
	hatchlings_emerged = db.Column(db.Integer)
	pipped_live = db.Column(db.Integer)
	pipped_dead = db.Column(db.Integer)
	
	# Eggs
	eggs_addled = db.Column(db.Integer)
	eggs_undeveloped = db.Column(db.Integer)
	eggs_sampled_for_sac = db.Column(db.Integer)
	eggs_embryo_1_4 = db.Column(db.Integer)
	eggs_embryo_2_4 = db.Column(db.Integer)
	eggs_embryo_3_4 = db.Column(db.Integer)
	eggs_embryo_4_4 = db.Column(db.Integer)
	eggs_damaged_raccoons = db.Column(db.Integer)
	eggs_damaged_ghost_crabs = db.Column(db.Integer)
	egg_damaged_plant_roots = db.Column(db.Integer)
	eggs_damaged_another_turtle = db.Column(db.Integer)
	eggs_damaged_bobcat = db.Column(db.Integer)
	eggs_damaged_other = db.Column(db.Integer)
	eggs_damaged_sea_oats = db.Column(db.Boolean)
	eggs_damaged_sea_purslane = db.Column(db.Boolean)
	eggs_damaged_railroad_vine = db.Column(db.Boolean)
	eggs_damaged_beach_sunflower = db.Column(db.Boolean)
	eggs_damaged_sea_grape = db.Column(db.Boolean)
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
	# Primary key
	morphometrics_id = db.Column(db.Integer, primary_key=True)

	# Foreign keys
	turtle_id = db.Column(db.Integer, db.ForeignKey('turtle.turtle_id'), nullable=False)
	encounter_id = db.Column(db.Integer, db.ForeignKey('encounter.encounter_id'), nullable=False)

	# Various fields
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
	flipper_damage = db.Column(db.Text)
	carapace_damage = db.Column(db.Text)

class Metadata(db.Model):
	# Primary key
	metadata_id = db.Column(db.Integer, primary_key=True)

	# Dependencies
	encounters = db.relationship('Encounter', backref='metadata')
	nets = db.relationship('Net', backref='metadata', lazy=True)
	incidental_captures = db.relationship('IncidentalCapture', backref='metadata')

	# Polymorphism
	type = db.Column(db.String(30))
	__mapper_args__ = {
		'polymorphic_identity': 'metadatas',
		'polymorphic_on': type
	}

class LagoonMetadata(Metadata):
	# Foreign key
	metadata_id = db.Column(db.Integer, db.ForeignKey('metadata.metadata_id'),primary_key=True, nullable=False)

	# Various fields
	metadata_date = db.Column(db.Date)
	metadata_location = db.Column(db.Text)
	metadata_investigators = db.Column(db.Text)
	number_of_cc_captured = db.Column(db.Integer)
	number_of_cm_captured = db.Column(db.Integer)
	number_of_other_captured = db.Column(db.Integer)

	# Environment
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

	# Polymorphism
	__mapper_args__ = {
		'polymorphic_identity': 'lagoon'
	}

class TridentMetadata(Metadata):
	# Foreign key
	metadata_id = db.Column(db.Integer, db.ForeignKey('metadata.metadata_id'), primary_key=True, nullable=False)

	# Various fields
	metadata_date = db.Column(db.Date)
	metadata_location = db.Column(db.Text)
	metadata_investigators = db.Column(db.Text)
	number_of_cc_captured = db.Column(db.Integer)
	number_of_cm_captured = db.Column(db.Integer)
	number_of_other_captured = db.Column(db.Integer)

	# Environment
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

	# Polymorphism
	__mapper_args__ = {
		'polymorphic_identity': 'trident'
	}

class OffshoreMetadata(Metadata):
	# Foreign key
	metadata_id = db.Column(db.Integer, db.ForeignKey('metadata.metadata_id'), primary_key=True, nullable=False)

	# Capture
	capture_date = db.Column(db.Date)
	capture_time = db.Column(db.Time)
	capture_latitude = db.Column(db.Float(5))
	capture_longitude = db.Column(db.Float(5))
	cloud_cover = db.Column(db.Text)
	seas = db.Column(db.Text)
	wind = db.Column(db.Text)
	capture_sargassum_water_temp = db.Column(db.Float(5))
	capture_open_water_temp = db.Column(db.Float(5))
	capture_air_temp = db.Column(db.Float(5))

	# Release
	release_latitude = db.Column(db.Float(5))
	release_longitude = db.Column(db.Float(5))
	release_time = db.Column(db.Time)
	release_sargassum_water_temp = db.Column(db.Float(5))
	sargassum_salinity = db.Column(db.Float(5))
	release_air_temp = db.Column(db.Float(5))
	release_open_water_temp = db.Column(db.Float(5))
	open_water_salinity = db.Column(db.Float(5))
	drifter_released = db.Column(db.Boolean)
	drifter1_id = db.Column(db.Text)
	drifter2_id = db.Column(db.Text)
	drifter1_type = db.Column(db.Text)
	drifter2_type = db.Column(db.Text)

	# Polymorphism
	__mapper_args__ = {
		'polymorphic_identity': 'offshore'
	}

class Encounter(db.Model):
	# Primary key
	encounter_id = db.Column(db.Integer, primary_key=True)

	# Foreign keys
	metadata_id = db.Column(db.Integer, db.ForeignKey('metadata.metadata_id'))
	turtle_id = db.Column(db.Integer, db.ForeignKey('turtle.turtle_id'), nullable=False)

	# Dependencies
	samples = db.relationship('Sample', backref='encounter')
	morphometrics = db.relationship('Morphometrics', uselist=False, backref='encounter')

	# Polymorphism
	type = db.Column(db.String(30))
	__mapper_args__ = {
		'polymorphic_identity': 'encounters',
		'polymorphic_on': type
	}

class Sample(db.Model):
	# Primary key
	sample_id = db.Column(db.Integer, primary_key=True)

	# Foreign key
	encounter_id = db.Column(db.Integer, db.ForeignKey('encounter.encounter_id'), nullable=False)

	# Dependencies
	tracking_entries = db.relationship('SampleTracking', backref='sample', lazy='joined')

	# Various fields
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

class TridentEncounter(Encounter):
	# Primary key
	encounter_id = db.Column(db.Integer, db.ForeignKey('encounter.encounter_id'), primary_key=True, nullable=False)
	
	# Fields common to all encounter types
	encounter_date = db.Column(db.Date)
	encounter_time = db.Column(db.Time)
	capture_type = db.Column(db.String(40))
	investigated_by = db.Column(db.String(500))
	entered_by = db.Column(db.String(30))
	entered_date = db.Column(db.Date)
	verified_by = db.Column(db.String(30))
	verified_date = db.Column(db.Date)
	notes = db.Column(db.Text)

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

	# Paps
	paps_present = db.Column(db.Boolean)
	pap_category = db.Column(db.Integer)
	paps_regression = db.Column(db.String(40))
	photos = db.Column(db.Boolean)
	pap_photos = db.Column(db.Boolean)

	# Polymorphism
	__mapper_args__ = {
		'polymorphic_identity': 'trident'
	}

class LagoonEncounter(Encounter):
	# Primary key
	encounter_id = db.Column(db.Integer, db.ForeignKey('encounter.encounter_id'), primary_key=True, nullable=False)

	# Fields common to all encounter types
	encounter_date = db.Column(db.Date)
	encounter_time = db.Column(db.Time)
	capture_type = db.Column(db.String(40))
	investigated_by = db.Column(db.String(500))
	entered_by = db.Column(db.String(30))
	entered_date = db.Column(db.Date)
	verified_by = db.Column(db.String(30))
	verified_date = db.Column(db.Date)
	notes = db.Column(db.Text)

	# Paps
	paps_present = db.Column(db.Boolean)
	pap_category = db.Column(db.Integer)
	paps_regression = db.Column(db.String(40))
	photos = db.Column(db.Boolean)
	pap_photos = db.Column(db.Boolean)

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
	encounter_id = db.Column(db.Integer, db.ForeignKey('encounter.encounter_id'), primary_key=True, nullable=False)

	# Fields common to all encounter types
	encounter_date = db.Column(db.Date)
	encounter_time = db.Column(db.Time)
	capture_type = db.Column(db.String(40))
	investigated_by = db.Column(db.String(500))
	entered_by = db.Column(db.String(30))
	entered_date = db.Column(db.Date)
	verified_by = db.Column(db.String(30))
	verified_date = db.Column(db.Date)

	# Fields unique to beach encounters
	prime_tag = db.Column(db.String(30))
	days_45 = db.Column(db.Date)
	days_70 = db.Column(db.Date)
	activity = db.Column(db.String(50))
	location_detail = db.Column(db.Text)
	location_NS = db.Column(db.String(1))
	latitude = db.Column(db.Float(5))
	longitude = db.Column(db.Float(5))
	site_description = db.Column(db.Text)
	notes = db.Column(db.Text)

	# DC Data
	outgoing_crawl_width = db.Column(db.Float(5))
	yolkless_collected = db.Column(db.Boolean)
	pink_spot_photo_taken = db.Column(db.Boolean)
	photo_taken_by = db.Column(db.Text)

	# Nest Markings
	dist_to_hidden_stake = db.Column(db.Float(5))
	hidden_stake_planted_in = db.Column(db.Text)
	dist_to_obvious_stake = db.Column(db.Float(5))
	obvious_stake_planted_in = db.Column(db.Text)
	dist_to_dune = db.Column(db.Float(5))
	dist_to_high_tide = db.Column(db.Float(5))
	can_buried = db.Column(db.Boolean)
	can_buried_NS = db.Column(db.String(1))
	sign_stake_in_place = db.Column(db.Boolean)
	scarp_over_46_cm = db.Column(db.Boolean)
	seaward_of_structure = db.Column(db.Boolean)
	within_1_m_of_structure = db.Column(db.Boolean)
	structure_description = db.Column(db.Text)

	# Paps
	paps_present = db.Column(db.Boolean)

	# Polymorphism
	__mapper_args__ = {
		'polymorphic_identity': 'beach'
	}

class Net(db.Model):
	# Primary key
	net_id = db.Column(db.Integer, primary_key=True)
	
	# Foreign key
	metadata_id = db.Column(db.Integer, db.ForeignKey('metadata.metadata_id'), nullable=False)

	# Various fields
	net_number = db.Column(db.Integer)
	net_deploy_start_time = db.Column(db.Time)
	net_deploy_end_time = db.Column(db.Time)
	net_retrieval_start_time = db.Column(db.Time)
	net_retrieval_end_time = db.Column(db.Time)

class IncidentalCapture(db.Model):
	# Primary key
	incidental_capture_id = db.Column(db.Integer, primary_key=True)

	# Foreign key
	metadata_id = db.Column(db.Integer, db.ForeignKey('metadata.metadata_id'), nullable=False)

	# Various fields
	species = db.Column(db.String(40))
	capture_time = db.Column(db.Time)
	measurement = db.Column(db.Text)
	notes = db.Column(db.Text)

class SampleTracking(db.Model):
	# Primary key
	sample_tracking_id = db.Column(db.Integer, primary_key=True)

	# Foreign key
	sample_id = db.Column(db.Integer, db.ForeignKey('sample.sample_id'), nullable=False)

	# Fields
	date = db.Column(db.Date)
	notes = db.Column(db.Text)

class NSRefuge(db.Model):
	# Primary key
	ns_refuge_id = db.Column(db.Integer, primary_key=True)

	# Dependencies
	# encounters = db.relationship('Encounter', backref='metadata')
	dc_crawls = db.relationship('DcCrawl', backref='ns_refuge')
	disorientations = db.relationship('Disorientation', backref='ns_refuge')
	depredations = db.relationship('Depredation', backref='ns_refuge')

	# Fields
	type = db.Column(db.String(10))
	date = db.Column(db.Date)
	initials = db.Column(db.String(30))
	notes = db.Column(db.Text)

	# # Km Fields
	# km_start = db.Column(db.Float(5))
	# km_end = db.Column(db.Float(5))
	# cc_nests = db.Column(postgresql.ARRAY(db.Integer),server_default='[]')
	# cc_fc = db.Column(postgresql.ARRAY(db.Integer),server_default='[]')
	# cm_nests = db.Column(postgresql.ARRAY(db.Integer),server_default='[]')
	# cm_fc = db.Column(postgresql.ARRAY(db.Integer),server_default='[]')

	# # BTO Fields
	# enginr = db.Column(db.Float(5))
	# natural = db.Column(db.Float(5))
	# enginr_cc_bto = db.Column(postgresql.ARRAY(db.Integer),server_default='[]')
	# enginr_cc_bto_lpac = db.Column(postgresql.ARRAY(db.Integer),server_default='[]')
	# enginr_cm_bto = db.Column(postgresql.ARRAY(db.Integer),server_default='[]')
	# enginr_cm_bto_lpac = db.Column(postgresql.ARRAY(db.Integer),server_default='[]')
	# natural_cc_bto = db.Column(postgresql.ARRAY(db.Integer),server_default='[]')
	# natural_cc_bto_lpac = db.Column(postgresql.ARRAY(db.Integer),server_default='[]')
	# natural_cm_bto = db.Column(postgresql.ARRAY(db.Integer),server_default='[]')
	# natural_cm_bto_lpac = db.Column(postgresql.ARRAY(db.Integer),server_default='[]')

	# Below HTL
	below_htl_cc_nest = db.Column(db.Integer)
	below_htl_cc_fc = db.Column(db.Integer)
	below_htl_cm_nest = db.Column(db.Integer)
	below_htl_cm_fc = db.Column(db.Integer)
	below_htl_dc_nest = db.Column(db.Integer)
	below_htl_dc_fc = db.Column(db.Integer)

	# Km Fields
	km_5_155_cc_nests = db.Column(db.Integer)
	km_5_155_cc_fc = db.Column(db.Integer)
	km_5_155_cm_nests = db.Column(db.Integer)
	km_5_155_cm_fc = db.Column(db.Integer)
	km_55_16_cc_nests = db.Column(db.Integer)
	km_55_16_cc_fc = db.Column(db.Integer)
	km_55_16_cm_nests = db.Column(db.Integer)
	km_55_16_cm_fc = db.Column(db.Integer)
	km_6_165_cc_nests = db.Column(db.Integer)
	km_6_165_cc_fc = db.Column(db.Integer)
	km_6_165_cm_nests = db.Column(db.Integer)
	km_6_165_cm_fc = db.Column(db.Integer)
	km_65_17_cc_nests = db.Column(db.Integer)
	km_65_17_cc_fc = db.Column(db.Integer)
	km_65_17_cm_nests = db.Column(db.Integer)
	km_65_17_cm_fc = db.Column(db.Integer)
	km_7_175_cc_nests = db.Column(db.Integer)
	km_7_175_cc_fc = db.Column(db.Integer)
	km_7_175_cm_nests = db.Column(db.Integer)
	km_7_175_cm_fc = db.Column(db.Integer)
	km_75_18_cc_nests = db.Column(db.Integer)
	km_75_18_cc_fc = db.Column(db.Integer)
	km_75_18_cm_nests = db.Column(db.Integer)
	km_75_18_cm_fc = db.Column(db.Integer)
	km_8_185_cc_nests = db.Column(db.Integer)
	km_8_185_cc_fc = db.Column(db.Integer)
	km_8_185_cm_nests = db.Column(db.Integer)
	km_8_185_cm_fc = db.Column(db.Integer)
	km_85_19_cc_nests = db.Column(db.Integer)
	km_85_19_cc_fc = db.Column(db.Integer)
	km_85_19_cm_nests = db.Column(db.Integer)
	km_85_19_cm_fc = db.Column(db.Integer)
	km_9_195_cc_nests = db.Column(db.Integer)
	km_9_195_cc_fc = db.Column(db.Integer)
	km_9_195_cm_nests = db.Column(db.Integer)
	km_9_195_cm_fc = db.Column(db.Integer)
	km_95_20_cc_nests = db.Column(db.Integer)
	km_95_20_cc_fc = db.Column(db.Integer)
	km_95_20_cm_nests = db.Column(db.Integer)
	km_95_20_cm_fc = db.Column(db.Integer)
	km_10_205_cc_nests = db.Column(db.Integer)
	km_10_205_cc_fc = db.Column(db.Integer)
	km_10_205_cm_nests = db.Column(db.Integer)
	km_10_205_cm_fc = db.Column(db.Integer)
	km_105_21_cc_nests = db.Column(db.Integer)
	km_105_21_cc_fc = db.Column(db.Integer)
	km_105_21_cm_nests = db.Column(db.Integer)
	km_105_21_cm_fc = db.Column(db.Integer)
	km_11_215_cc_nests = db.Column(db.Integer)
	km_11_215_cc_fc = db.Column(db.Integer)
	km_11_215_cm_nests = db.Column(db.Integer)
	km_11_215_cm_fc = db.Column(db.Integer)
	km_115_22_cc_nests = db.Column(db.Integer)
	km_115_22_cc_fc = db.Column(db.Integer)
	km_115_22_cm_nests = db.Column(db.Integer)
	km_115_22_cm_fc = db.Column(db.Integer)
	km_12_225_cc_nests = db.Column(db.Integer)
	km_12_225_cc_fc = db.Column(db.Integer)
	km_12_225_cm_nests = db.Column(db.Integer)
	km_12_225_cm_fc = db.Column(db.Integer)
	km_125_23_cc_nests = db.Column(db.Integer)
	km_125_23_cc_fc = db.Column(db.Integer)
	km_125_23_cm_nests = db.Column(db.Integer)
	km_125_23_cm_fc = db.Column(db.Integer)
	km_13_235_cc_nests = db.Column(db.Integer)
	km_13_235_cc_fc = db.Column(db.Integer)
	km_13_235_cm_nests = db.Column(db.Integer)
	km_13_235_cm_fc = db.Column(db.Integer)
	km_135_24_cc_nests = db.Column(db.Integer)
	km_135_24_cc_fc = db.Column(db.Integer)
	km_135_24_cm_nests = db.Column(db.Integer)
	km_135_24_cm_fc = db.Column(db.Integer)
	km_14_245_cc_nests = db.Column(db.Integer)
	km_14_245_cc_fc = db.Column(db.Integer)
	km_14_245_cm_nests = db.Column(db.Integer)
	km_14_245_cm_fc = db.Column(db.Integer)
	km_145_25_cc_nests = db.Column(db.Integer)
	km_145_25_cc_fc = db.Column(db.Integer)
	km_145_25_cm_nests = db.Column(db.Integer)
	km_145_25_cm_fc = db.Column(db.Integer)
	km_15_255_cc_nests = db.Column(db.Integer)
	km_15_255_cc_fc = db.Column(db.Integer)
	km_15_255_cm_nests = db.Column(db.Integer)
	km_15_255_cm_fc = db.Column(db.Integer)

	# BTO Fields
	enginr = db.Column(db.Float(5))
	enginr_cc_below = db.Column(db.Integer)
	enginr_cc_tran = db.Column(db.Integer)
	enginr_cc_on = db.Column(db.Integer)
	enginr_cc_b_l = db.Column(db.Integer)
	enginr_cc_b_p = db.Column(db.Integer)
	enginr_cc_b_ac = db.Column(db.Integer)
	enginr_cc_t_l = db.Column(db.Integer)
	enginr_cc_t_p = db.Column(db.Integer)
	enginr_cc_t_ac = db.Column(db.Integer)
	enginr_cc_o_l = db.Column(db.Integer)
	enginr_cc_o_p = db.Column(db.Integer)
	enginr_cc_o_ac = db.Column(db.Integer)
	enginr_cm_below = db.Column(db.Integer)
	enginr_cm_tran = db.Column(db.Integer)
	enginr_cm_on = db.Column(db.Integer)
	enginr_cm_b_l = db.Column(db.Integer)
	enginr_cm_b_p = db.Column(db.Integer)
	enginr_cm_b_ac = db.Column(db.Integer)
	enginr_cm_t_l = db.Column(db.Integer)
	enginr_cm_t_p = db.Column(db.Integer)
	enginr_cm_t_ac = db.Column(db.Integer)
	enginr_cm_o_l = db.Column(db.Integer)
	enginr_cm_o_p = db.Column(db.Integer)
	enginr_cm_o_ac = db.Column(db.Integer)
	natural = db.Column(db.Float(5))
	natural_cc_below = db.Column(db.Integer)
	natural_cc_tran = db.Column(db.Integer)
	natural_cc_on = db.Column(db.Integer)
	natural_cc_b_l = db.Column(db.Integer)
	natural_cc_b_p = db.Column(db.Integer)
	natural_cc_b_ac = db.Column(db.Integer)
	natural_cc_t_l = db.Column(db.Integer)
	natural_cc_t_p = db.Column(db.Integer)
	natural_cc_t_ac = db.Column(db.Integer)
	natural_cc_o_l = db.Column(db.Integer)
	natural_cc_o_p = db.Column(db.Integer)
	natural_cc_o_ac = db.Column(db.Integer)
	natural_cm_below = db.Column(db.Integer)
	natural_cm_tran = db.Column(db.Integer)
	natural_cm_on = db.Column(db.Integer)
	natural_cm_b_l = db.Column(db.Integer)
	natural_cm_b_p = db.Column(db.Integer)
	natural_cm_b_ac = db.Column(db.Integer)
	natural_cm_t_l = db.Column(db.Integer)
	natural_cm_t_p = db.Column(db.Integer)
	natural_cm_t_ac = db.Column(db.Integer)
	natural_cm_o_l = db.Column(db.Integer)
	natural_cm_o_p = db.Column(db.Integer)
	natural_cm_o_ac = db.Column(db.Integer)

class DcCrawl(db.Model):
	# Primary Key
	dc_crawl_id = db.Column(db.Integer, primary_key=True)
	
	# Foreign key
	ns_refuge_id = db.Column(db.Integer, db.ForeignKey('ns_refuge.ns_refuge_id'), nullable=False)

	# Fields
	km = db.Column(db.Float(5))
	type = db.Column(db.String(10))

class Disorientation(db.Model):
	# Primary Key
	disorientation_id = db.Column(db.Integer, primary_key=True)

	# Foreign key
	ns_refuge_id = db.Column(db.Integer, db.ForeignKey('ns_refuge.ns_refuge_id'), nullable=False)

	# Fields
	km = db.Column(db.Float(5))
	adult = db.Column(db.String(10))
	hatchling = db.Column(db.String(10))

class Depredation(db.Model):
	# Primary Key
	depredation_id = db.Column(db.Integer, primary_key=True)

	# Foreign key
	ns_refuge_id = db.Column(db.Integer, db.ForeignKey('ns_refuge.ns_refuge_id'), nullable=False)

	# Fields
	species = db.Column(db.String(30))
	km = db.Column(db.Float(5))
	predator = db.Column(db.String(30))
	eggs_destroyed = db.Column(db.Integer)
	stake = db.Column(db.Integer)

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

	# tags = ma.Nested(TagSchema, attribute='turtle') 
	# tags = fields.Nested(TagSchema, data_key='turtle_id')
	# tags = fields.Nested(TagSchema, many=True)
	# tags = fields.List(fields.Nested(TagSchema, many=True)) 

	# # Keys
	# encounter_id = fields.Int()
	# lagoon_encounter_id = fields.Int()
	# metadata_id = fields.Int()
	# turtle_id = fields.Int()

	# # # Dependencies
	# # samples = ma.Nested(SampleTrackingSchema)
	# # morphometrics = ma.Nested(MorphometricsSchema)

	# # # Fields common to all encounter types
	# # encounter_date = fields.Date()
	# # encounter_time = fields.Time()
	# # investigated_by = fields.Str()
	# # entered_by = fields.Str()
	# # entered_date = fields.Date()
	# # verified_by =  fields.Str()
	# # verified_date =  fields.Date()
	# # notes =  fields.Str()

	# # # Paps
	# # paps_present = fields.Boolean()
	# # pap_category = fields.Int()
	# # paps_regression = fields.Str()
	# # photos = fields.Boolean()
	# # pap_photos = fields.Boolean()

	# # # Fields unique to lagoon encounters
	# # living_tags = fields.Boolean()
	# # other = fields.Str()
	# # leeches = fields.Boolean()
	# # leeches_where = fields.Str()
	# # leech_eggs = fields.Boolean()
	# # leech_eggs_where = fields.Str()
