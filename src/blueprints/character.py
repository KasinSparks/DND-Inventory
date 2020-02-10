from flask import (
	Blueprint, g, redirect, render_template, request, session, url_for, current_app
)

import os

from ..db import get_db, query_db

from .auth import login_required

from ..image_sever import convert_image_to_base64

import math

bp = Blueprint('character', __name__, url_prefix='/character')

# Character select screen
@bp.route('select')
@login_required
def character_select():
	# Query DB for a list of user's characters
	sql_str = """SELECT Character_ID, Character_Name
				FROM Character
				WHERE Character.User_ID = ?;
				"""

	characters = query_db(sql_str, (session['user_id'],))

	return render_template('character/character_select.html',
							characters=characters)

# Character page
@bp.route('/<int:char_id>')
@login_required
def character_page(char_id):

	# Check for user_id associated with char_id
	sql_str = """SELECT *
				FROM Character
				WHERE Character.User_ID = ? AND Character.Character_ID = ?;
				"""

	characters = query_db(sql_str, (session['user_id'], char_id), True, True)

	if characters is None:
		# Error
		redirect(url_for('character.character_select'))

	item_id_list = [
		characters['Character_Helmet'], characters['Character_Shoulders'], characters['Character_Chest'],
		characters['Character_Gloves'],characters['Character_Leggings'],characters['Character_Boots'],
		 characters['Character_Trinket1'], characters['Character_Trinket2'],characters['Character_Ring1'],
		characters['Character_Ring2'],characters['Character_Magic_Item1'],characters['Character_Magic_Item2'],
		characters['Character_Weapon1'], characters['Character_Weapon2'], characters['Character_Weapon3'],
		characters['Character_Weapon4']
	] 

	# Query DB for character's items and equipment

	equiped_item_short_data = {
		'head' : item_short_data(characters['Character_Helmet'], 'Head', 'Item_img.png'),
		'shoulder' : item_short_data(characters['Character_Shoulders'], 'Shoulder', 'Item_img_shoulders.png'),
		'chest' : item_short_data(characters['Character_Chest'], 'Torso', 'Item_img_chest.png'),
		'hand' : item_short_data(characters['Character_Gloves'], 'Hand', 'Item_img_glove.png'),
		'leg' : item_short_data(characters['Character_Leggings'], 'Leg', 'Item_img_leggings.png'),
		'boots' : item_short_data(characters['Character_Boots'], 'Foot', 'Item_img_boots.png'),
		'trinket1' : item_short_data(characters['Character_Trinket1'], 'Trinket', 'Item_img_trinket.png'),
		'trinket2' : item_short_data(characters['Character_Trinket2'], 'Trinket', 'Item_img_trinket.png'),
		'ring1' : item_short_data(characters['Character_Ring1'], 'Ring', 'Item_img_ring.png'),
		'ring2' : item_short_data(characters['Character_Ring2'], 'Ring', 'Item_img_ring.png'),
		'item1' : item_short_data(characters['Character_Magic_Item1'], 'Item', 'Item_img_item.png'),
		'item2' : item_short_data(characters['Character_Magic_Item2'], 'Item', 'Item_img_item.png'),
		'weapon1' : item_short_data(characters['Character_Weapon1'], 'Main Hand', 'Item_img_weapon.png'),
		'offhand1' : item_short_data(characters['Character_Weapon2'], 'Off Hand', 'Item_img_offhand.png'),
		'weapon2' : item_short_data(characters['Character_Weapon3'], 'Main Hand', 'Item_img_weapon.png'),
		'offhand2' : item_short_data(characters['Character_Weapon4'], 'Off Hand', 'Item_img_offhand.png')
	}

	sql_str = """SELECT Class_Name
				From Class
				WHERE Class_ID = ?;
			"""
	class_name = query_db(sql_str, (characters['Character_Class'],), True, True)
	if class_name is None or class_name == '':
		class_name = 'No Class'
	else:
		class_name = class_name['Class_Name'] 

	sql_str = """SELECT Alignment_Name
				From Alignments
				WHERE Alignment_ID = ?;
			"""
	alignment_name = query_db(sql_str, (characters['Character_Alignment'],), True, True)
	if alignment_name is None or alignment_name == '':
		alignment_name = 'No Alignment'
	else:
		alignment_name = alignment_name['Alignment_Name']

	stat_bonus = sumation_stats(item_id_list)

	image_data = convert_image_to_base64(os.path.join(current_app.config['IMAGE_UPLOAD'], characters['Character_Image']))
	#image_data = convert_image_to_base64(characters['Character_Image'])

	character_data = {
		'name' : shorten_string(characters['Character_Name'], 20),
		'class' : shorten_string(class_name, 12),
		'level' : convert_form_field_data_to_int(characters['Character_Level']),
		'hp' : convert_form_field_data_to_int(characters['Character_HP']),
		'max_hp' : convert_form_field_data_to_int(characters['Character_Max_HP']) + stat_bonus['health'],
		'ac' : convert_form_field_data_to_int(characters['Character_AC']) + stat_bonus['ac'],
		'initiative' : convert_form_field_data_to_int(characters['Character_Initiative']) + stat_bonus['initiative'],
		'attack_bonus' : convert_form_field_data_to_int(characters['Character_Attack_Bonus']) + stat_bonus['attack'],
		'alignment' : shorten_string(alignment_name, 12),
		'currency' : convert_form_field_data_to_int(characters['Character_Currency']),
		'weight' : convert_form_field_data_to_int(characters['Character_Base_Carrying_Cap']),
		'max_weight' : convert_form_field_data_to_int(characters['Character_Max_Carry_Weight']),
		'str' : convert_form_field_data_to_int(characters['Character_Strength']) + stat_bonus['str'],
		'dex' : convert_form_field_data_to_int(characters['Character_Dexterity']) + stat_bonus['dex'],
		'con' : convert_form_field_data_to_int(characters['Character_Constitution']) + stat_bonus['con'],
		'int' : convert_form_field_data_to_int(characters['Character_Intelligence']) + stat_bonus['int'],
		'wis' : convert_form_field_data_to_int(characters['Character_Wisdom']) + stat_bonus['wis'],
		'cha' : convert_form_field_data_to_int(characters['Character_Charisma']) + stat_bonus['cha'],
		'image' : image_data['encoded_image'],
		'image_type' : image_data['image_type'] 
	}

	stat_modifiers = {
		'str' :	calculate_modifier(character_data['str']), 
		'dex' :	calculate_modifier(character_data['dex']),
		'con' :	calculate_modifier(character_data['con']),
		'int' :	calculate_modifier(character_data['int']),
		'wis' :	calculate_modifier(character_data['wis']),
		'cha' :	calculate_modifier(character_data['cha'])
	}

	inv_items = get_inv_items(char_id, item_id_list)

	for k in inv_items:
		for i in inv_items[k]:
			character_data['weight'] += i['Item_Weight']

	return render_template('character_page.html',
							char_id=char_id,
							equiped_item=equiped_item_short_data,
							character_data=character_data,
							stat_modifiers=stat_modifiers,
							inv_items=inv_items)


def get_inv_items(char_id : int, equiped_items_ids):
	items = {}
	
	sql_str = """SELECT Items.Item_ID, Items.Item_Weight, Items.Item_Name, Rarities.Rarities_Color, Slots.Slots_Name
				FROM Inventory
				INNER JOIN Items on Inventory.Item_ID=Items.Item_ID
				INNER JOIN Rarities on Rarities.Rarities_ID=Items.Rarity_ID
				INNER JOIN Slots on Items.Item_Slot=Slots.Slots_ID
				WHERE Inventory.Character_ID = ?;
			"""
	query_result = query_db(sql_str, (char_id,), True)

	for q in query_result:
		if q['Slots_Name'] not in items.keys():
			items[q['Slots_Name']] = []
		
		item_fields = {
			'Item_ID' : q['Item_ID'],
			'Item_Weight' : q['Item_Weight'],
			'Item_Name' : q['Item_Name'],
			'Rarities_Color' : q['Rarities_Color'],
			'Slots_Name' : q['Slots_Name'],
			'Is_Equiped' : True if q['Item_ID'] in equiped_items_ids else False
		}

		items[q['Slots_Name']].append(item_fields)

	return items

def calculate_modifier(stat_value):
	return math.ceil((stat_value - 11) / 2)

def item_short_query(item_id):
	sql_str = """SELECT Items.Item_Name, Rarities.Rarities_Color, Items.Item_Picture
				FROM Items
				INNER JOIN Rarities ON Items.Rarity_ID = Rarities.Rarities_ID
				WHERE Items.Item_ID = ?;
			"""
	return query_db(sql_str, (item_id,), True, True)

def item_stat_query(item_id):
	sql_str = """SELECT Items.Item_Str_Bonus, Items.Item_Dex_Bonus, Items.Item_Con_Bonus,
				Items.Item_Int_Bonus, Items.Item_Wis_Bonus, Items.Item_Cha_Bonus,
				Items.Item_Attack_Bonus, Items.Item_Initiative_Bonus, Items.Item_Health_Bonus,
				Items.Item_AC_Bonus
				FROM Items
				WHERE Items.Item_ID = ?;
			"""
	return query_db(sql_str, (item_id,), True, True)

def sumation_stats(item_id_list):
	stat_bonus = {
		'str' : 0,
		'dex' : 0,
		'con' : 0,
		'int' : 0,
		'wis' : 0,
		'cha' : 0,
		'attack' : 0,
		'initiative' : 0,
		'health' : 0,
		'ac' : 0,
	}

	for item_id in item_id_list:
		query_result = item_stat_query(item_id)
		if query_result is not None:
			stat_bonus['str'] += convert_form_field_data_to_int(query_result['Item_Str_Bonus'])
			stat_bonus['dex'] += convert_form_field_data_to_int(query_result['Item_Dex_Bonus'])
			stat_bonus['con'] += convert_form_field_data_to_int(query_result['Item_Con_Bonus'])
			stat_bonus['int'] += convert_form_field_data_to_int(query_result['Item_Int_Bonus'])
			stat_bonus['wis'] += convert_form_field_data_to_int(query_result['Item_Wis_Bonus'])
			stat_bonus['cha'] += convert_form_field_data_to_int(query_result['Item_Cha_Bonus'])
			stat_bonus['attack'] += convert_form_field_data_to_int(query_result['Item_Attack_Bonus'])
			stat_bonus['initiative'] += convert_form_field_data_to_int(query_result['Item_Initiative_Bonus'])
			stat_bonus['health'] += convert_form_field_data_to_int(query_result['Item_Health_Bonus'])
			stat_bonus['ac'] += convert_form_field_data_to_int(query_result['Item_AC_Bonus'])

	return stat_bonus

def item_short_data(item_id, default_name, defalut_image_name):
	item_data = {
		'name' : default_name,
		'image' : convert_image_to_base64(os.path.join('src', 'static', 'images', defalut_image_name)),
		'rarity_color' : None 
	}

	if item_id is None or item_id < 1:
		# No item
		return item_data
	
	item = item_short_query(item_id)
	
	if item['Item_Name'] is not None and item['Item_Name'] != '':
		item_data['name'] = shorten_string(item['Item_Name'], 17)

	if item['Item_Picture'] is not None and item['Item_Picture'] != '' and item['Item_Picture'] != 'no_image.png':
		item_data['image'] = convert_image_to_base64(os.path.join(current_app.config['IMAGE_UPLOAD'], item['Item_Picture']))
	else:
		item_data['image'] = convert_image_to_base64(os.path.join('src', 'static', 'images', item['Item_Picture']))


	if item['Rarities_Color'] is not None and item['Rarities_Color'] != '':
		item_data['rarity_color'] = item['Rarities_Color']

	return item_data

def shorten_string(string : str, max_length : int):
	shortened_name = string

	if len(string) > max_length:
		shortened_name = string[0:max_length] + '...'
	
	return shortened_name


# Character create screen
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create_character():
	# TODO: add variables so users do not have to reenter data if error occurs

	# Get all the race types
	sql_str = """SELECT Race_Name
				FROM Races
				"""
	races = query_db(sql_str)
	
	# Get all the class types
	sql_str = """SELECT Class_Name
				FROM Class 
				"""
	classes = query_db(sql_str)
	
	# Get all the alignment types
	sql_str = """SELECT Alignment_Name
				FROM Alignments 
				"""
	alignments = query_db(sql_str)

	return render_template('character/character_create.html',
							races=races,
							classes=classes,
							alignments=alignments)

def convert_form_field_data_to_int(field_data):
	return 0 if field_data is None or field_data == '' else int(field_data)


# Submit a new character
@bp.route('/create/submit', methods=('GET', 'POST'))
@login_required
def create_character_submit():
	# TODO: data type and value checks
	if request.method == 'POST':
		# Add the data to the DB

		## TODO: clean this up
		data = {
			'race_name' : request.form['race'],
			'race_id' : None,
			'class_name' : request.form['class'],
			'class_id' : None,
			'alignment_name' : request.form['alignment'],
			'alignment_id' : None,
			'level' : convert_form_field_data_to_int(request.form['level']), 
			'base_carrying_cap' : convert_form_field_data_to_int(request.form['base_carrying_cap']),
			'strength' : convert_form_field_data_to_int(request.form['strength']),
			'dexerity' : convert_form_field_data_to_int(request.form['dexerity']),
			'constitution' : convert_form_field_data_to_int(request.form['constitution']),
			'intelligence' : convert_form_field_data_to_int(request.form['intelligence']),
			'wisdom' : convert_form_field_data_to_int(request.form['wisdom']),
			'charisma' : convert_form_field_data_to_int(request.form['charisma']),
			'health_points' : convert_form_field_data_to_int(request.form['health_points'])
		}

		error = None 

		# Check form data
		name_length = len(str(request.form['name']))
		if name_length < 1 or name_length > 25:
			error = "ERROR: Invaild name length of {}. ".format(name_length)

		# Check if user already has a character with the same name
		sql_str = """SELECT Character_Name
					FROM Character
					WHERE User_ID = ? AND Character_Name = ?;
				"""
		char_with_same_name = query_db(sql_str, (session['user_id'], request.form['name']), True, True)

		if char_with_same_name is not None:
			error = "ERROR: You already have a character with this name! "

		
		if error is None:

			# Check if new race, class, or alignment need to be inserted into the DB
			if request.form['race_other'] is not None and request.form['race_other'] != '':
				sql_str = """SELECT Race_Name
						FROM Races
						WHERE Race_Name = ?"""
				race_in_db = query_db(sql_str, (request.form['race_other'],), True, True)

				if race_in_db is None:
					sql_str = """INSERT INTO Races (Race_Name)
								VALUES (?);
							"""
					query_db(sql_str, (request.form['race_other'],), False)
				data['race_name'] = request.form['race_other']

			if request.form['class_other'] is not None and request.form['class_other'] != '':
				sql_str = """SELECT Class_Name
						FROM Class 
						WHERE Class_Name = ?"""
				class_in_db = query_db(sql_str, (request.form['class_other'],), True, True)

				if class_in_db is None:
					sql_str = """INSERT INTO Class (Class_Name)
								VALUES (?);
							"""
					query_db(sql_str, (request.form['class_other'],), False)
				data['class_name'] = request.form['class_other']

			if request.form['alignment_other'] is not None and request.form['alignment_other'] != '':
				sql_str = """SELECT Alignment_Name
						FROM Alignments 
						WHERE Alignment_Name = ?"""
				alignment_in_db = query_db(sql_str, (request.form['alignment_other'],), True, True)

				if alignment_in_db is None:
					sql_str = """INSERT INTO Alignments (Alignment_Name)
								VALUES (?);
							"""
					query_db(sql_str, (request.form['alignment_other'],), False)
				data['alignment_name'] = request.form['alignment_other']


			sql_str = """SELECT Race_ID
						FROM Races
						WHERE Race_Name = ?;"""

			data['race_id'] = int(query_db(sql_str, (data['race_name'],), True, True)['Race_ID'])

			sql_str = """SELECT Class_ID
						FROM Class 
						WHERE Class_Name = ?;"""
			data['class_id'] = int(query_db(sql_str, (data['class_name'],), True, True)['Class_ID'])

			sql_str = """SELECT Alignment_ID
						FROM Alignments 
						WHERE Alignment_Name = ?;"""
			data['alignment_id'] = int(query_db(sql_str, (data['alignment_name'],), True, True)['Alignment_ID'])


			sql_str = """INSERT INTO Character
						(User_ID, Character_Name, Character_Class, Character_Race,
						Character_Level, Character_Base_Carrying_Cap, Character_Strength,
						Character_Dexterity, Character_Constitution, Character_Intelligence,
						Character_Wisdom, Character_Charisma, Character_HP, Character_Max_HP, Character_Alignment)
						VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
					"""
			query_db(sql_str, (session['user_id'], request.form['name'], data['class_id'], data['race_id'],
								data['level'], data['base_carrying_cap'], data['strength'],
								data['dexerity'], data['constitution'], data['intelligence'],
								data['wisdom'], data['charisma'], data['health_points'],
								data['health_points'], data['alignment_id']), False)
			

			sql_str = """SELECT Character_ID
						FROM Character
						WHERE User_ID = ? AND Character_Name = ?;
					"""			
			char_id = query_db(sql_str, (session['user_id'], request.form['name']), True, True)['Character_ID']

			return redirect(url_for('character.character_page', char_id=char_id)) 
	
	# TODO: add variables so users do not have to reenter data if error occurs
	return redirect(url_for('character.create_character'))


@bp.route('/edit/class/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_class(char_id):
	sql_str = """SELECT Character_ID
				FROM Character
				WHERE User_ID = ? AND Character_ID = ?;
			"""
	has_char = query_db(sql_str, (session['user_id'], char_id), True, True)

	if has_char is None:
		print('User does not have character with user id.')
		return '400'

	if request.method == 'POST':
		new_val = request.form['value']

		sql_str = """SELECT Class_ID
				FROM Class;
				"""
		class_ids = query_db(sql_str)
		class_ids = [x['Class_ID'] for x in class_ids]

		try:
			new_val = int(new_val)
		except:
			new_val = -1

		if new_val not in class_ids:
			print('NO class with id. ')
			return '400'
		
		sql_str = """UPDATE	Character
				SET Character_Class = ?
				WHERE User_ID = ? AND Character_ID = ?; 
				"""
		query_db(sql_str, (new_val, session['user_id'], char_id), False)
			
		sql_str = """SELECT Class_Name
					FROM Class
					WHERE Class_ID = ?;
				"""
		class_name = query_db(sql_str, (new_val,), True, True)['Class_Name']
		return class_name



	return '200'