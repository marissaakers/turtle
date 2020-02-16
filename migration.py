import csv
from datetime import datetime
import psycopg2
import time

filename = "2019db.csv"
rows = []

###################################
#### Indices of the DB Columns ####
###################################
#   0: turtle_id									= Turtle ID
#   1: Encounter_ID 								= Encounter ID
#   2: Clutch_ID 									= Clutch ID
#   3: Morphometrics::Morphometrics_ID 				= Morphometrics ID
#   4: Environment_ID 								= Environment ID
#   5: StudyType 									= encounter type
#   6: Species 										= Species (all data sheets)
#   7: Tag_#_Linear_All 							= Tag list (all data sheets)
#   8: Date Encountered 							= Date (all data sheets)
#   9: Date Adjusted Flag 							= ?
#  10: Time as text 								= Time (all data sheets)
#  11: Time anomaly 								= Discard, just used to say that the time is missing
#  12: Latitude 									= Latitude (beach data sheet)
#  13: Longitude 									= Longitude (beach data sheet)
#  14: Location_Detail 								= Location (beach data sheet)
#  15: Investigators 								= MTRG members
#  16: StrangeEncounter 							= See below
#  17: Recaptured 									= With above, this will fill in "capture type" (new, recap, strange recap)
#  18: Recapture Linear Dates 						= not currently on data sheets, can be queried
#  19: TagScar 										= tag scar fields (all data sheets)
#  20: Pit_Scan 									= pit scan field (all data sheets)
#  21: Turtle_Photographed 							= PHOTOS
#  22: No Samples Collected 						= legacy field
#  23: Papillomas 									= boolean
#  24: Pap Category 								= num_paps
#  25: PapsRegressed 								= regression
#  26: Pap photo 									= PAP PHOTOS
#  27: PapMapped 									= legacy field
#  28: PapillomaDescription 						= legacy field
#  29: Leeches 										= leeches
#  30: Leech_Eggs 									= leech eggs
#  31: Leech_Notes 									= not a direct fit but we'll put it in "leeches: where"
#  32: Disposal_of_Specimen 						= legacy field
#  33: Flipper_Damage 								= flipper damage
#  34: Shell_Damage 								= shell damage
#  35: Notes 										= notes
#  36: Activity 									= activity (beach)
#  37: Stake Summary 								= legacy field
#  38: Survery Full Location 						= legacy field
#  39: ClutchDeposited 								= clutch deposited
#  40: ClutchMoved 									= legacy field
#  41: Sand Description 							= sand type
#  42: Nest Placement 								= placement
#  43: ClutchFate 									= legacy field
#  44: Eggs Yolked 									= legacy field
#  45: Eggs Broken 									= legacy field
#  46: Egg CluthSize_Sum 							= legacy field
#  47: Eggs Yolkless 								= legacy field
#  48: Eggs Research 								= legacy field
#  49: Distance_to_HiddenStake 						= hidden stake
#  50: Distance_to_ObviousStake 					= obvious stake
#  51: Distance_to_Dune 							= distance to dune
#  52: Distance_to_HighTide 						= distance to high tide
#  53: InPlace_Stakes 								= sign stake in place (beach sheet NOT clutch sheet)
#  54: InPlace_Foil 								= legacy field
#  55: InPlace_Metal 								= legacy field
#  56: Morphometrics::Morphometrics_ID 				= morphometrics id, not needed
#  57: Morphometrics::Carap_L_oc Over barnacles		= boolean legacy field
#  58: Morphometrics::Carap_L_oc 					= curved length
#  59: Morphometrics::Carap_L_sl 					= straight length
#  60: Morphometrics::Carap_L_min 					= minimum length
#  61: Morphometrics::Carap_L_Greatest 				= legacy field
#  62: Morphometrics::Carap_W_oc Over barnacles 	= boolean legacy field
#  63: Morphometrics::Carap_W_oc					= curvied width
#  64: Morphometrics::Carap_W_sl 					= straight width
#  65: Morphometrics::Plastron_L over barnacles 	= boolean legacy field
#  66: Morphometrics::Plastron_L 					= plastron length
#  67: Morphometrics::Tail_L_Pl_Vent 				= tail length PL vent
#  68: Morphometrics::Tail_L_Pl_Tip 				= tail length PL tip
#  69: Morphometrics::Head_Width 					= head width
#  70: Morphometrics::Body_Depth over barnacles 	= boolean legacy field
#  71: Morphometrics::Body_Depth 					= body depth
#  72: Morphometrics::Weight 						= weight
#  73: Morphometrics::Sex 							= legacy field
#  74: Morphometrics::Cloaca_Temp 					= float
#  75: Morphometrics::InteranalScute				= boolean
#  76: Clutch_ID 									= Clutch ID
#  77: Clutch::Date_Laid 							= legacy field
#  78: Clutch::Date_Emerged 						= emergence date (beach data sheet)
#  79: Clutch::Date_Inventory 						= inventoried date (beach data sheet)
#  80: Clutch::Inventoried by  						= inventoried by (beach data sheet)
#  81: Clutch::a5_Emergence 						= emergence? (beach data sheet)
#  82: Clutch::Cans in place choice 				= Cans in place? (beach data sheet)
#  83: Clutch::Predated choice 						= Predated (beach data sheet)
#  84: Clutch::Wash over 							= Washed over (beach data sheet)
#  85: Clutch::Poached 								= Poached (beach data sheet)
#  86: Clutch::a_Hatched_Eggs 						= Hatched (beach data sheet)
#  87: Clutch::a2_Live_In_Nest 						= Live (beach data sheet)
#  88: Clutch::a3_Dead_In_Nest  					= Dead (beach data sheet)
#  89: Clutch::a_calc_Total Emergence 				= Hatchlings Emerged (beach data sheet)
#  90: Clutch::b1_Pipped_Live 						= Pipped Live (beach data sheet)
#  91: Clutch::b2_Pipped_dead 						= Pipped Dead (beach data sheet)
#  92: Clutch::b_calc_Pipped_Total 					= not on data sheet, but just sum of 2 above
#  93: Clutch::c1_Embryo 							= not on data sheet?
#  94: Clutch::c2_Fetus 							= legacy field
#  95: Clutch::c4.1_Embryo 1_4 developed 			= 1/4 embryo (beach data sheet)
#  96: Clutch::c4.2_Embryo 2_4 developed 			= 2/4 embryo (beach data sheet)
#  97: Clutch::c4.3_Embryo 3_4 developed  			= 3/4 embryo (beach data sheet)
#  98: Clutch::c4.4_Embryo 4_4 developed 			= full embryo (beach data sheet)
#  99: Clutch::c5_Addled 							= addled (beach data sheet)
# 100: Clutch::c6_Infertile_eggs 					= legacy field
# 101: Clutch::c_calc_Total Arrested 				= some kind of sum
# 102: Clutch::d1_Research 							= legacy field
# 103: Clutch::d2_Poached 							= legacy field
# 104: Clutch::d3_Raccoons 							= raccoons
# 105: Clutch::d4_Another Turtle 					= another turtle
# 106: Clutch::d5_Ghost_Crabs 						= ghost crabs
# 107: Clutch::d6_Bobcat 							= bobcat
# 108: Clutch::d7_Plant_Roots 						= plant roots
# 109: Clutch::d8_Other_EggAffect 					= other 
# 110: Clutch::d7.Roots1 Beach sunflower 			= ... below
# 111: Clutch::d7.Roots2 Railroad Vine 				= ... below
# 112: Clutch::d7.Roots3 Sea grape 					= Plant roots
# 113: Clutch::d7.Roots4 Sea Oats 					= ... above
# 114: Clutch::d7.Roots5 Sea Purslane 				= ... above
# 115: Clutch::d_calc_Total Destroyed 				= sum of something
# 116: Clutch::e1_Broken_Eggs Inventory count 		= broken
# 117: Clutch::e2_Washout 							= washout
# 118: Clutch::e3_Inundated 						= legacy field
# 119: Clutch::e_Calc Total Other Loss 				= some kind of sum
# 120: Clutch::f1_Yolkless_Eggs Inventory Count 	= sum of below 2 fields
# 121: Clutch::f2_Hydrated Yolkless_Eggs 			= yolkless hydrated
# 122: Clutch::f3_Dehydrated Yolkless_Eggs 			= yolkless dehydrated
# 123: Clutch::calc_Total Clutch 					= just a sum here
# 124: Sand Description 							= substrate
# 125: Clutch::Comments								= notes
# 126: Clutch::d_Nest_Disturbed summary 			= legacy field
# 127: Clutch::Nest data collection problems		= legacy field
# 128: Environment::•Environment_ID 				= environment id
# 129: Environment::Time weather as Text 			= time
# 130: Environment::EstimatedTime_Flag 				= useless boolean
# 131: Environment::Weather_Conditions 				= weather
# 132: Environment::Air_temp 						= air temp
# 133: Environment::Wind Direction 					= wind direction
# 134: Environment::WindSpeed Min MPH 				= legacy field
# 135: Environment::WindSpeed Max MPH 				= legacy field
# 136: Environment::WindSpeed Min mps 				= legacy field
# 137: Environment::WindSpeed Max mps 				= legacy field
# 138: Environment::Depth 							= legacy field
# 139: Environment::Length Units 					= legacy field
# 140: Environment::WaterTemp0						= water temp surface (metadata)
# 141: Environment::WaterTemp1 						= water temp 1m (metadata)
# 142: Environment::WaterTemp2 						= water temp 2m (metadata)
# 143: Environment::WaterTemp3 						= water temp 3m (metadata)
# 144: Environment::WaterTemp6 						= water temp 6m (metadata)
# 145: Environment::WaterTempBottom 				= water temp bottom (metadata)
# 146: Environment::Salinity0 						= salinity surface (metadata)
# 147: Environment::Salinity1 						= salinity 1m (metadata)
# 148: Environment::Salinity2 						= salinity 2m (metadata)
# 149: Environment::Salinity3 						= salinity 3m (metadata)
# 150: Environment::Salinity6 						= salinity 6m (metadata)
# 151: Environment::SalinityBottom 					= salinity bottom (metadata)
# 152: Environment::Secchi Depth 					= legacy field
# 153: Environment::Secchi Distance from shore 		= legacy field
# 154: Environment::Time Text High_Tide 			= legacy field
# 155: Environment::Time Text Low_Tide 				= legacy field
# 156: Environment::Notes_Environment 				= legacy field
def main():
	start_time = time.time()
	conn = create_connection()

	# open the csv file into a python variable
	with open(filename, 'r') as csvfile:

		#create csv reader
		csvreader = csv.reader(csvfile)

		# add each row to our rows list
		for row in csvreader:
			rows.append(row)

	# iterate over each row and parse the fields
	for row in rows[1:]:

		old_turtle_id = row[0]
		morphometrics_id = None if not row[3] else row[3]
		encounter_type = row[5]
		species = row[6]

		# index 7 is the column containing the turtle's tags
		# the row may also contain the string "TURTLE NOT TAGGED"
		tags = []
		if row[7][:6].upper() != "TURTLE":
			# if the row actually contains tags, turn them into a list
			split_row = row[7].split(" ")
			tags = split_row[:len(split_row)-1]
		else:
			tags = None

		print(row[8])
		encounter_date = None if not row[8] else datetime.strptime(row[8], '%m/%d/%Y') # e.g. 01/01/2020
		encounter_time = None if not row[10] else datetime.strptime(row[10], '%H:%M') # e.g. 13:25

		latitude = None if not row[12] else row[12]
		longitude = None if not row[13] else row[13]
		location_detail = None if not row[14] else row[14]

		investigated_by = row[15]

		strange_encounter = False if not row[16] else True
		recaptured = False if not row[17] else True
		if row[17]:
			if row[16]:
				capture_type = 'STRANGE RECAP'
			else:
				capture_type = 'RECAP'
		else:
			capture_type = 'NEW'

		tag_scar = row[19]
		pit_scan = row[20]
		turtle_photographed = row[21]
		no_samples_collected = row[22]

		# paps
		paps = False if not row[23] else True
		# -1 is a spcial pap category for unreported cases
		if row[24].upper() == 'UNREPORTED':
			pap_category = -1
		else:
			pap_category = row[24] if row[24] in ('0', '1', '2', '3') else None
		paps_regressed = 'No' if not row[25] else 'Yes'
		pap_photo = False if not row[26] else True

		leeches = False if not row[29] else True
		leech_eggs = False if not row[30] else True
		leech_notes = row[31]
		flipper_damage = row[33]
		shell_damage = row[34]
		notes = row[35]
		activity = row[36]

		clutch_deposited = False if (not row[39] or row[39][:2].upper() == 'NO') else True
		sand_type = row[41]
		nest_placement = row[42]


		distance_to_hidden_stake = None if not row[49] else row[49]
		distance_to_obvious_stake = None if not row[50] else row[50]
		distance_to_dune = None if not row[51] else row[51]
		distance_to_high_tide = None if not row[52] else row[52]

		stakes_in_place = False if not row[53] else True

		curved_length = None if not row[58] else row[58]
		straight_length = None if not row[59] else row[59]
		minimum_length = None if not row[60] else row[60]
		curved_width = None if not row[63] else row[63]
		straight_width = None if not row[64] else row[64]
		plastron_length = None if not row[66] else row[66]
		tail_length_pl_vent = None if not row[67] else row[67]
		tail_length_pl_tip = None if not row[68] else row[68]
		head_width = None if not row[69] else row[69]
		body_depth = None if not row[71] else row[71]
		weight = None if not row[72] else row[72]

		emergence_date = None if not row[78] else datetime.strptime(row[78], '%m/%d/%Y')
		inventoried_date = None if not row[79] else datetime.strptime(row[79], '%m/%d/%Y')
		inventoried_by = row[80]
		emergence = False if not row[81] else True

		# Cans in place: currently a text field with North, South, both or none.
		# We can parse the content and make two fields out of it
		s_can_in_place = True if row[82].upper().find("N") != -1 else False
		n_can_in_place = True if row[82].upper().find("S") != -1 else False

		# Predated: boolean
		predated = False if not row[83] else True

		# Washed over: boolean
		washed_over = False if not row[84] else True

		# Poached: boolean
		poached = False if not row[85] else True

		# Hatched: integer
		hatched = None if not row[86] else row[86]

		# Live hatchlings: integer
		live_hatchlings = None if not row[87] else row[87]

		# Dead hatchlings: integer
		dead_hatchlings = None if not row[88] else row[88]

		# Hatchlings emerged: integer
		hatchlings_emerged = None if not row[89] else row[89]

		# Pipped live: integer
		pipped_live = None if not row[90] else row[90]

		# Pipped dead: integer
		pipped_dead = None if not row[91] else row[91]

		# Embryo fields: integers
		embryo_1_4 = None if not row[95] else row[95]
		embryo_2_4 = None if not row[96] else row[96]
		embryo_3_4 = None if not row[97] else row[97]
		embryo_4_4 = None if not row[98] else row[98]

		# Addled: integer
		addled = None if not row[99] else row[99]

		# All integers
		raccoons = None if not row[104] else row[104]
		another_turtle = None if not row[105] else row[105]
		ghost_crabs = None if not row[106] else row[106]
		bobcats = None if not row[107] else row[107]

		# SKIP FOR NOW, gotta figure out a good way to do this
		# clutch_plant_roots = row[108]
		# clutch_other_egg_affecte = row[109]
		# clutch_roots_beach_sunflower = row[110]
		# clutch_roots_railroad_vine = row[111]
		# clutch_roots_sea_grape = row[112]
		# clutch_roots_sea_oats = row[113]
		# clutch_roots_sea_purslane = row[114]

		# Broken: integer
		broken = None if not row[116] else row[116]

		# Washout: integer
		washout = None if not row[117] else row[117]

		# Hydrated and dehydrated: integers
		yolkless_hydrated = None if not row[121] else row[121]
		yolkless_dehydrated = None if not row[122] else row[122]
	
		# Substrate: text
		substrate = row[124]
		
		# Clutch_notes: text
		clutch_notes = row[125]

		# Environment stuff
		environment_time = None if not row[129] else datetime.strptime(row[129], '%H:%M')
		weather = row[131]
		air_temp = None if not row[132] else row[132]
		wind_dir = row[133]
		water_temp_surface = None if not row[140] else row[140]
		water_temp_1_m = None if not row[141] else row[141]
		water_temp_2_m = None if not row[142] else row[142]
		water_temp_6_m = None if not row[144] else row[144]
		water_temp_bottom = None if not row[145] else row[145]
		salinity_surface = None if not row[146] else row[146]
		salinity_1_m = None if not row[147] else row[147]
		salinity_2_m = None if not row[148] else row[148]
		salinity_6_m = None if not row[150] else row[150]
		salinity_bottom = None if not row[151] else row[151]

		##### All fields below are just sums of other columns and will be discarded #####
		# 101: Clutch::c_calc_Total Arrested 
		# clutch_total_destroyed = row[115]
		# 119: Clutch::e_Calc Total Other Loss
		# 120: Clutch::f1_Yolkless_Eggs Inventory Count
		# 123: Clutch::calc_Total Clutch

		##### All fields below are legacy and will be dealt with later #####
		#  18: Recapture Linear Dates
		#  22: No Samples Collected
		#  27: PapMapped
		#  28: PapillomaDescription
		#  32: Disposal_of_Specimen
		#  37: Stake Summary
		#  38: Survery Full Location
		#  40: ClutchMoved
		#  43: ClutchFate
		#  44: Eggs Yolked 
		#  45: Eggs Broken
		#  46: Egg CluthSize_Sum
		#  47: Eggs Yolkless
		#  48: Eggs Research
		#  54: InPlace_Foil
		#  55: InPlace_Metal
		#  57: Morphometrics::Carap_L_oc Over barnacles
		#  61: Morphometrics::Carap_L_Greatest
		#  62: Morphometrics::Carap_W_oc Over barnacles
		#  65: Morphometrics::Plastron_L over barnacles
		#  70: Morphometrics::Body_Depth over barnacles
		#  73: Morphometrics::Sex
		#  74: Morphometrics::Cloaca_Temp
		#  75: Morphometrics::InteranalScute
		#  77: Clutch::Date_Laid
		#  93: Clutch::c1_Embryo
		#  94: Clutch::c2_Fetus
		# 100: Clutch::c6_Infertile_eggs
		# 102: Clutch::d1_Research
		# 103: Clutch::d2_Poached
		# 117: Clutch::e2_Washout
		# 118: Clutch::e3_Inundated
		# 126: Clutch::d_Nest_Disturbed summary
		# 127: Clutch::Nest data collection problems
		# 130: Environment::EstimatedTime_Flag
		# 134: Environment::WindSpeed Min MPH
		# 135: Environment::WindSpeed Max MPH
		# 136: Environment::WindSpeed Min mps
		# 137: Environment::WindSpeed Max mps
		# 138: Environment::Depth
		# 139: Environment::Length Units
		# 143: Environment::WaterTemp3
		# 149: Environment::Salinity3
		# 152: Environment::Secchi Depth
		# 153: Environment::Secchi Distance from shore
		# 154: Environment::Time Text High_Tide
		# 155: Environment::Time Text Low_Tide
		# 156: Environment::Notes_Environment

		##### CHECK IF TURTLE EXISTS #####
		cursor = conn.cursor()
		query = ('SELECT turtle_id, old_turtle_id FROM turtle WHERE old_turtle_id = {0}').format(old_turtle_id)
		cursor.execute(query)
		turtle_info = cursor.fetchone()

		if turtle_info is None:
			##### INSERT TURTLE #####
			turtle_fields = (old_turtle_id, species)
			# cursor = conn.cursor()
			query = ('INSERT INTO turtle (old_turtle_id, species) VALUES {0}').format(turtle_fields)
			cursor.execute(query)
			conn.commit()

			##### QUERY TURTLE FOR IDs #####
			# cursor = conn.cursor()
			query = ('SELECT turtle_id, old_turtle_id FROM turtle ORDER BY turtle_id DESC LIMIT 1')
			cursor.execute(query)
			turtle_info = cursor.fetchone() # turtle_id = turtle_info[0], old_turtle_id = turtle_info[1]

		##### INSERT TAGS #####
		if tags is not None:
			for tag in tags:
				##### CHECK IF TAG EXISTS #####
				query = ('SELECT tag_id FROM tag WHERE tag_number = {0}').format('\'' + tag + '\'')
				cursor.execute(query)
				result = cursor.fetchone()

				##### ONLY INSERT IF NOT IN DB ALREADY #####
				if result is None:
					tag_fields = (turtle_info[0], tag)
					query = ('INSERT INTO tag (turtle_id, tag_number) VALUES {0}').format(tag_fields)
					cursor.execute(query)
					conn.commit()

		##### INSERT CLUTCH #####
		if clutch_deposited == True:
			clutch_fields = (turtle_info[0], clutch_deposited, sand_type, nest_placement, emergence_date,
							inventoried_date, emergence, s_can_in_place, n_can_in_place, predated, washed_over,
							poached, inventoried_by, hatched, live_hatchlings, dead_hatchlings, hatchlings_emerged,
							pipped_live, pipped_dead, addled, embryo_1_4, embryo_2_4, embryo_3_4, embryo_4_4,
							raccoons, ghost_crabs, another_turtle, bobcats, broken, washout, yolkless_hydrated,
							yolkless_dehydrated, substrate, clutch_notes)
			query = ('''INSERT INTO clutch (turtle_id, clutch_deposited, sand_type, placement, emergence_date, inventory_date,
											emergence, s_can_in_place, n_can_in_place, predated, washed_over, poached,
											inventoried_by, hatched, live_hatchlings, dead_hatchlings, hatchlings_emerged,
											pipped_live, pipped_dead, eggs_addled, eggs_embryo_1_4, eggs_embryo_2_4, eggs_embryo_3_4,
											eggs_embryo_4_4, eggs_damaged_raccoons, eggs_damaged_ghost_crabs, eggs_damaged_another_turtle,
											eggs_damaged_bobcat, eggs_broken, eggs_washout, eggs_yolkless_hydrated, eggs_yolkless_dehydrated, 
											substrate, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
											%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''')
			cursor.execute(query, clutch_fields)
			conn.commit()

		# metadata_id defaults to None to account for beach encounters which have no metadata
		metadata_id = None

		##### CHECK FOR EXISTING METADATA ENTRY #####
		if encounter_type.upper()[0:5] != 'BEACH':
			query = ('SELECT metadata_id FROM metadata WHERE metadata_date = {0}').format('\'' + datetime.strftime(encounter_date, '%m/%d/%Y') + '\'')
			cursor.execute(query)
			result = cursor.fetchone()

			##### NO METADATA YET, MAKE A NEW ENTRY #####
			if result is None:
				metadata_fields = (environment_time, weather, air_temp, water_temp_surface, water_temp_1_m, water_temp_2_m, water_temp_6_m,
									water_temp_bottom, salinity_surface, salinity_1_m, salinity_2_m, salinity_6_m, salinity_bottom, encounter_date)
				query = ('''INSERT INTO metadata (environment_time, weather, air_temp, water_temp_surface, water_temp_1_m,
										water_temp_2_m, water_temp_6_m, water_temp_bottom, salinity_surface, salinity_1_m,
										salinity_2_m, salinity_6_m, salinity_bottom, metadata_date) VALUES (%s, %s, %s, %s, %s, %s, %s,
										%s, %s, %s, %s, %s, %s, %s)''')
				cursor.execute(query, metadata_fields)
				conn.commit()

				##### GRAB NEW METADATA ID #####
				query = ('SELECT metadata_id FROM metadata WHERE metadata_date = {0}').format('\'' + datetime.strftime(encounter_date, '%m/%d/%Y') + '\'')
				cursor.execute(query)
				metadata_id = cursor.fetchone()[0]

			##### USE EXISTING ENTRY #####
			else:
				metadata_id = result[0]

		##### INSERT COMMON ENCOUNTER FIELDS #####
		encounter_fields = (turtle_info[0], metadata_id, encounter_date, encounter_time, investigated_by, notes, paps, 
			pap_category, paps_regressed, pap_photo)
		query = ('''INSERT INTO encounter (turtle_id, metadata_id, encounter_date, encounter_time, investigated_by,
											notes, paps_present, pap_category, paps_regression, pap_photos) VALUES (%s, %s, %s,
											%s, %s, %s, %s, %s, %s, %s)''')
		cursor.execute(query, encounter_fields)
		conn.commit()

		##### GRAB ENCOUNTER ID #####
		query = ('SELECT encounter_id FROM encounter ORDER BY encounter_id DESC LIMIT 1')
		cursor.execute(query)
		encounter_id = cursor.fetchone()[0]

		##### BEACH ENCOUNTER #####
		if encounter_type.upper()[0:5] == 'BEACH':
			##### SET ENCOUNTER TYPE #####
			query = ('UPDATE encounter SET type = \'beach\' WHERE encounter_id = {0}').format(encounter_id)
			cursor.execute(query)
			conn.commit()

			##### INSERT BEACH ENCOUNTER FIELDS #####
			beach_encounter_fields = (capture_type, activity, location_detail, latitude, longitude, distance_to_hidden_stake,
									distance_to_obvious_stake, distance_to_high_tide, distance_to_dune, encounter_id)
			query = ('''INSERT INTO beach_encounter (capture_type, activity, location_detail, latitude, longitude, dist_to_hidden_stake,
													dist_to_obvious_stake, dist_to_high_tide, dist_to_dune, encounter_id) VALUES
													(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''')
			cursor.execute(query, beach_encounter_fields)
			conn.commit()


		##### LAGOON ENCOUNTER #####
		if encounter_type.upper()[0:6] == 'LAGOON':
			##### SET ENCOUNTER TYPE #####
			query = ('UPDATE encounter SET type = \'lagoon\' WHERE encounter_id = {0}').format(encounter_id)
			cursor.execute(query)
			conn.commit()

			##### INSERT LAGOON ENCOUNTER FIELDS #####
			lagoon_fields = (encounter_id, leeches, leech_eggs, leech_notes)
			query = ('''INSERT INTO lagoon_encounter (encounter_id, leeches, leech_eggs, leeches_where) VALUES (%s,
									%s, %s, %s)''')
			cursor.execute(query, lagoon_fields)
			conn.commit()


		##### TRIDENT ENCOUNTER #####
		if encounter_type.upper()[0:7] == 'TRIDENT':
			##### SET ENCOUNTER TYPE #####
			query = ('UPDATE encounter SET type = \'trident\' WHERE encounter_id = {0}').format(encounter_id)
			cursor.execute(query)
			conn.commit()

			##### INSERT TRIDENT ENCOUNTER FIELDS #####
			trident_fields = (encounter_id, leeches, leech_eggs, leech_notes)
			query = ('''INSERT INTO trident_encounter (encounter_id, leeches, leech_eggs, leeches_where) VALUES (%s,
									%s, %s, %s)''')
			cursor.execute(query, trident_fields)
			conn.commit()

		##### INSERT MORPHOMETRICS FIELDS #####
		if morphometrics_id is not None:
			morphometrics_fields = (turtle_info[0], encounter_id, curved_length, straight_length, minimum_length, curved_width,
									straight_width, plastron_length, tail_length_pl_vent, tail_length_pl_tip, head_width,
									body_depth, weight)
			query = ('''INSERT INTO morphometrics (turtle_id, encounter_id, curved_length, straight_length, minimum_length, curved_width,
													straight_width, plastron_length, tail_length_pl_vent, tail_length_pl_tip, head_width,
													body_depth, weight) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''')
			cursor.execute(query, morphometrics_fields)
			conn.commit()

	conn.close()
	end_time = time.time()
	print('Execution took {0} seconds.'.format(end_time - start_time))


def create_connection():
	connection = psycopg2.connect(user="turtle",
									password="avQ^EC6^Zi&n8k)$n1l9",
									host="turtledb.csc2iayec306.us-east-2.rds.amazonaws.com",
									port="5432",
									database="postgres")
	return connection

	# try:
	# 	conn = sqlite3.connect(db_file)
	# 	return conn
	# except Error as e:
	# 	print(e)
	# finally:
	# 	if conn:
	# 		conn.close()

	# return None

# run main() when we run the program
if __name__ == "__main__":
	main()
