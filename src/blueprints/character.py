from flask import (
	Blueprint, g, redirect, render_template, request, session, url_for, current_app, jsonify
)

from werkzeug.utils import secure_filename

import os

from db import get_db, query_db

from blueprints.auth import login_required

from image_sever import convert_image_to_base64

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
		return redirect(url_for('character.character_select'))

	item_id_list = [
		characters['Character_Head'], characters['Character_Shoulder'], characters['Character_Torso'],
		characters['Character_Hand'],characters['Character_Leg'],characters['Character_Foot'],
		 characters['Character_Trinket1'], characters['Character_Trinket2'],characters['Character_Ring1'],
		characters['Character_Ring2'],characters['Character_Item1'],characters['Character_Item2'],
		characters['Character_Weapon1'], characters['Character_Weapon2'], characters['Character_Weapon3'],
		characters['Character_Weapon4']
	] 

	# Query DB for character's items and equipment

	equiped_item_short_data = {
		'head' : item_short_data(characters['Character_Head'], 'Head', 'Item_img.png'),
		'shoulder' : item_short_data(characters['Character_Shoulder'], 'Shoulder', 'Item_img_Shoulder.png'),
		'Torso' : item_short_data(characters['Character_Torso'], 'Torso', 'Item_img_torso.png'),
		'hand' : item_short_data(characters['Character_Hand'], 'Hand', 'Item_img_hand.png'),
		'leg' : item_short_data(characters['Character_Leg'], 'Leg', 'Item_img_leg.png'),
		'Foot' : item_short_data(characters['Character_Foot'], 'Foot', 'Item_img_foot.png'),
		'trinket1' : item_short_data(characters['Character_Trinket1'], 'Trinket', 'Item_img_trinket.png'),
		'trinket2' : item_short_data(characters['Character_Trinket2'], 'Trinket', 'Item_img_trinket.png'),
		'ring1' : item_short_data(characters['Character_Ring1'], 'Ring', 'Item_img_ring.png'),
		'ring2' : item_short_data(characters['Character_Ring2'], 'Ring', 'Item_img_ring.png'),
		'item1' : item_short_data(characters['Character_Item1'], 'Item', 'Item_img_item.png'),
		'item2' : item_short_data(characters['Character_Item2'], 'Item', 'Item_img_item.png'),
		'weapon1' : item_short_data(characters['Character_Weapon1'], 'Weapn1', 'Item_img_weapon.png'),
		'offhand1' : item_short_data(characters['Character_Weapon2'], 'Weapon2', 'Item_img_offhand.png'),
		'weapon2' : item_short_data(characters['Character_Weapon3'], 'Weapon3', 'Item_img_weapon.png'),
		'offhand2' : item_short_data(characters['Character_Weapon4'], 'Weapon4', 'Item_img_offhand.png')
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

	#image_data = convert_image_to_base64(os.path.join(current_app.config['IMAGE_UPLOAD'], characters['Character_Image']))
	#image_data = convert_image_to_base64(characters['Character_Image'])
	image_data = url_for('static', filename='images/no_image.png')

	if characters['Character_Image'] is not None and characters['Character_Image'] != '' and characters['Character_Image'] != 'no_image.png':
		image_data = '/dataserver/imageserver/user/' + characters['Character_Image']

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
		#'max_weight' : convert_form_field_data_to_int(characters['Character_Max_Carry_Weight']),
		'max_weight' : 15 * (convert_form_field_data_to_int(characters['Character_Strength']) + stat_bonus['str']),
		'str' : convert_form_field_data_to_int(characters['Character_Strength']) + stat_bonus['str'],
		'dex' : convert_form_field_data_to_int(characters['Character_Dexterity']) + stat_bonus['dex'],
		'con' : convert_form_field_data_to_int(characters['Character_Constitution']) + stat_bonus['con'],
		'int' : convert_form_field_data_to_int(characters['Character_Intelligence']) + stat_bonus['int'],
		'wis' : convert_form_field_data_to_int(characters['Character_Wisdom']) + stat_bonus['wis'],
		'cha' : convert_form_field_data_to_int(characters['Character_Charisma']) + stat_bonus['cha'],
		'image' : image_data,
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
		for i in inv_items[k]['items']:
			character_data['weight'] += int(i['Item_Weight']) * int(i['Amount'])

	sql_str = """
		"""

	return render_template('character_page.html',
							char_id=char_id,
							equiped_item=equiped_item_short_data,
							character_data=character_data,
							stat_modifiers=stat_modifiers,
							inv_items=inv_items
						)


def get_inv_items(char_id : int, equiped_items_ids):
	items = {}

	sql_str = """SELECT *
				FROM SLOTS;
		"""
	slots = query_db(sql_str)

	for slot in slots:
		items[slot['Slots_Name']] = {
			'id' : slot['Slots_ID'],
			'equipable' : slot['Slots_Equipable'],
			'items' : []
		}
	
	sql_str = """SELECT Items.Item_ID, Items.Item_Weight, Items.Item_Name, Rarities.Rarities_Color, Slots.Slots_Name, Inventory.Amount
				FROM Inventory
				INNER JOIN Items on Inventory.Item_ID=Items.Item_ID
				INNER JOIN Rarities on Rarities.Rarities_ID=Items.Rarity_ID
				INNER JOIN Slots on Items.Item_Slot=Slots.Slots_ID
				WHERE Inventory.Character_ID = ?;
			"""
	query_result = query_db(sql_str, (char_id,), True)

	for q in query_result:
		#if q['Slots_Name'] not in items.keys():
		#	items[q['Slots_Name']] = []
		
		item_fields = {
			'Item_ID' : q['Item_ID'],
			'Item_Weight' : q['Item_Weight'],
			'Item_Name' : q['Item_Name'],
			'Rarities_Color' : q['Rarities_Color'],
			'Amount' : q['Amount'],
			#'Slots_Name' : q['Slots_Name'],
			#'Slots_ID' : q['Slots_ID'],
			'Is_Equiped' : True if q['Item_ID'] in equiped_items_ids else False
		}

		items[q['Slots_Name']]['items'].append(item_fields)

	print(items)

	return items

def calculate_modifier(stat_value):
	return math.floor((stat_value - 10) / 2)

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
				Items.Item_AC_Bonus, Items.Item_Damage_Num_Of_Dices, Items.Item_Damage_Num_Of_Dice_Sides
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
		'num_of_dices' : 0,
		'num_of_dice_sides' : 0
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
			stat_bonus['num_of_dices'] += convert_form_field_data_to_int(query_result['Item_Damage_Num_Of_Dices'])
			stat_bonus['num_of_dice_sides'] += convert_form_field_data_to_int(query_result['Item_Damage_Num_Of_Dice_Sides'])

	return stat_bonus

def item_short_data(item_id, default_name, defalut_image_name):
	item_data = {
		'name' : default_name,
		#'image' : convert_image_to_base64(os.path.join('src', 'static', 'images', defalut_image_name)),
		'image' : url_for('static', filename='images/' + defalut_image_name),
		'rarity_color' : None 
	}

	if item_id is None or item_id < 1:
		# No item
		return item_data
	
	item = item_short_query(item_id)
	
	if item['Item_Name'] is not None and item['Item_Name'] != '':
		item_data['name'] = shorten_string(item['Item_Name'], 17)

	#if item['Item_Picture'] is not None and item['Item_Picture'] != '' and item['Item_Picture'] != 'no_image.png':
	#	item_data['image'] = convert_image_to_base64(os.path.join(current_app.config['IMAGE_UPLOAD'], item['Item_Picture']))
	#else:
	#	item_data['image'] = convert_image_to_base64(os.path.join('src', 'static', 'images', item['Item_Picture']))
	if item['Item_Picture'] is not None and item['Item_Picture'] != '' and item['Item_Picture'] != 'no_image.png':
		item_data['image'] = '/dataserver/imageserver/item/' + item['Item_Picture']


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


def check_if_user_has_character(user_id, char_id):
	sql_str = """SELECT Character_ID
				FROM Character
				WHERE User_ID = ? AND Character_ID = ?;
			"""
	has_char = query_db(sql_str, (user_id, char_id), True, True)

	if has_char is not None:
		return True 
	
	return False

@bp.route('/edit/class/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_class(char_id):
	if not check_if_user_has_character(session['user_id'], char_id):
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



@bp.route('/edit/alignment/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_alignment(char_id):
	if not check_if_user_has_character(session['user_id'], char_id):
		return '400'


	if request.method == 'POST':
		new_val = request.form['value']

		sql_str = """SELECT Alignment_ID
				FROM Alignments;
				"""
		class_ids = query_db(sql_str)
		class_ids = [x['Alignment_ID'] for x in class_ids]

		try:
			new_val = int(new_val)
		except:
			new_val = -1

		if new_val not in class_ids:
			print('NO alignment with id. ')
			return '400'
		
		sql_str = """UPDATE	Character
				SET Character_Alignment = ?
				WHERE User_ID = ? AND Character_ID = ?; 
				"""
		query_db(sql_str, (new_val, session['user_id'], char_id), False)
			
		sql_str = """SELECT Alignment_Name
					FROM Alignments
					WHERE Alignment_ID = ?;
				"""
		class_name = query_db(sql_str, (new_val,), True, True)['Alignment_Name']
		return class_name



	return '200'

@bp.route('/edit/level/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_level(char_id):
	if not check_if_user_has_character(session['user_id'], char_id):
		return '400'

	if request.method == 'POST':
		new_val = request.form['value']

		try:
			new_val_int = int(new_val)
		except:
			new_val_int = 0

		sql_str = """UPDATE	Character
				SET Character_Level = ?
				WHERE User_ID = ? AND Character_ID = ?; 
				"""
		query_db(sql_str, (new_val_int, session['user_id'], char_id), False)
		
		#return new_val 
		return jsonify(character_level=new_val)



	return '200'

@bp.route('/edit/currency/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_currency(char_id):
	if not check_if_user_has_character(session['user_id'], char_id):
		return '400'

	if request.method == 'POST':
		new_val = request.form['value']

		try:
			new_val_int = int(new_val)
		except:
			new_val_int = 0

		sql_str = """UPDATE	Character
				SET Character_Currency = ?
				WHERE User_ID = ? AND Character_ID = ?; 
				"""
		query_db(sql_str, (new_val_int, session['user_id'], char_id), False)
		
		#return new_val 
		return jsonify(character_currency=new_val)



	return '200'


@bp.route('/edit/image/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_image(char_id):
	if not check_if_user_has_character(session['user_id'], char_id):
		return '400'

	if request.method == 'POST':
		if 'image' not in request.files:
			return 'No file included'

		
		new_img = request.files['image']

		if new_img.filename == '':
			return 'File name was blank'

		if new_img and allowed_file(new_img.filename):
			filename = secure_filename(new_img.filename)
			dirName = os.path.join('users', str(session['user_id']))
			fullDirName = os.path.join(current_app.config['IMAGE_UPLOAD'], dirName)

			if not os.path.exists(fullDirName):
				os.mkdir(fullDirName, mode=0o770)

			new_img.save(os.path.join(fullDirName, filename))

			sql_str = """UPDATE Character
						SET Character_Image=?
						WHERE Character_ID=?;
					"""
			query_db(sql_str, (filename, char_id), False)

			return redirect(url_for('character.character_page', char_id=char_id)) 

		return 'Not in allowed file types or image was None' 

	return '400'

def allowed_file(filename):
	 return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@bp.route('/edit/health/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_health(char_id):
	if not check_if_user_has_character(session['user_id'], char_id):
		return '400'

	if request.method == 'POST':
		new_val = request.form['value']

		try:
			new_val = int(new_val)
		except:
			new_val = 0

		sql_str = """SELECT Character_Max_HP
					FROM Character
					WHERE User_ID = ? AND Character_ID = ?;
				"""
		max_hp = query_db(sql_str, (session['user_id'], char_id), True, True)['Character_Max_HP']

		if new_val > max_hp:
			new_val = max_hp

		sql_str = """UPDATE	Character
				SET Character_HP = ?
				WHERE User_ID = ? AND Character_ID = ?; 
				"""
		query_db(sql_str, (new_val, session['user_id'], char_id), False)
		
		return jsonify(character_hp=new_val)

	return '200'

def edit_field(char_id, character_field : str, item_field : str):
	if not check_if_user_has_character(session['user_id'], char_id):
		# TODO: change this to a exception later
		return 0
		#return '400'

	if request.method == 'POST':
		new_val = request.form['value']

		try:
			new_val = int(new_val)
		except:
			new_val = 0

		sql_str = """UPDATE	Character
				SET """ + character_field + """ = ?
				WHERE User_ID = ? AND Character_ID = ?; 
				"""
		query_db(sql_str, (new_val, session['user_id'], char_id), False)


		sql_str = """SELECT *
			FROM Character
			WHERE Character_ID = ?;
			"""
		characters = query_db(sql_str, (char_id,), True, True)

		item_id_list = [
			characters['Character_Head'], characters['Character_Shoulder'], characters['Character_Torso'],
			characters['Character_Hand'],characters['Character_Leg'],characters['Character_Foot'],
			characters['Character_Trinket1'], characters['Character_Trinket2'],characters['Character_Ring1'],
			characters['Character_Ring2'],characters['Character_Item1'],characters['Character_Item2'],
			characters['Character_Weapon1'], characters['Character_Weapon2'], characters['Character_Weapon3'],
			characters['Character_Weapon4']
		]

		stat_additional = 0

		for i in item_id_list:
			sql_str = """SELECT """ + item_field + """
					FROM Items
					WHERE Item_ID = ?;
					""" 
			item = query_db(sql_str, (i,), True, True)
			if item is not None:
				stat_additional += item[item_field]

		return  (new_val + stat_additional)

	return 0
	#return '200'


@bp.route('/edit/maxhealth/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_maxhealth(char_id):
	val = edit_field(char_id, 'Character_Max_HP', 'Item_Health_Bonus')
	return jsonify(character_max_hp=val)

@bp.route('/edit/ac/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_ac(char_id):
	val = edit_field(char_id, 'Character_AC', 'Item_AC_Bonus')
	return jsonify(character_ac=val)

@bp.route('/edit/initiative/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_initiative(char_id):
	val = edit_field(char_id, 'Character_Initiative', 'Item_Initiative_Bonus')	
	return jsonify(character_initiative=val)

@bp.route('/edit/attackBonus/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_attack_bonus(char_id):
	val = edit_field(char_id, 'Character_Attack_Bonus', 'Item_Attack_Bonus')	
	return jsonify(character_attack_bonus=val)


@bp.route('/edit/str/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_str(char_id):
	val = edit_field(char_id, 'Character_Strength', 'Item_Str_Bonus')	
	return jsonify(
			character_str=val,
			character_max_weight=val * 15,
			character_str_mod=calculate_modifier(val)
		)

@bp.route('/edit/dex/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_dex(char_id):
	val = edit_field(char_id, 'Character_Dexterity', 'Item_Dex_Bonus')	
	return jsonify(
			character_dex=val,
			character_dex_mod=calculate_modifier(val)
		)

@bp.route('/edit/con/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_con(char_id):
	val = edit_field(char_id, 'Character_Constitution', 'Item_Con_Bonus')	
	return jsonify(
			character_con=val,
			character_con_mod=calculate_modifier(val)
		)

@bp.route('/edit/int/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_int(char_id):
	val = edit_field(char_id, 'Character_Intelligence', 'Item_Int_Bonus')	
	return jsonify(
			character_int=val,
			character_int_mod=calculate_modifier(val)
		)

@bp.route('/edit/wis/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_wis(char_id):
	val = edit_field(char_id, 'Character_Wisdom', 'Item_Wis_Bonus')	
	return jsonify(
			character_wis=val,
			character_wis_mod=calculate_modifier(val)
		)

@bp.route('/edit/cha/<int:char_id>', methods=('GET', 'POST'))
@login_required
def edit_cha(char_id):
	val = edit_field(char_id, 'Character_Charisma', 'Item_Cha_Bonus')	
	return jsonify(
			character_cha=val,
			character_cha_mod=calculate_modifier(val)
		)

@bp.route('/add/items/<int:char_id>', methods=('GET', 'POST'))
@login_required
def add_items(char_id):
	weight = 0 

	if request.method == 'POST':
		if not check_if_user_has_character(session['user_id'], char_id):
			# TODO: change this to a exception later
			return 0
			#return '400

		

		
		for line in request.form:
			sql_str = """SELECT Amount, Items.Item_Weight
						FROM Inventory
						LEFT JOIN Items ON Items.Item_ID=Inventory.Item_ID
						WHERE Character_ID = ? AND Inventory.Item_ID = ?;
					"""
			try:
				item_id = int(line)
				prev_amount_query = query_db(sql_str, (char_id, item_id), True, True)
				prev_amount = 0

				numberOfItems = int(request.form[line])
				if numberOfItems > 0:
					if prev_amount_query is not None:
						prev_amount = int(prev_amount_query['Amount'])
						sql_str = """UPDATE Inventory
								SET Amount = ?
								WHERE Character_ID = ? AND Item_ID = ?;
								"""
						query_db(sql_str, (prev_amount + numberOfItems, char_id, line), False)
					else:
						sql_str = """INSERT INTO Inventory (Character_ID,Item_ID,Amount)
									VALUES (?,?,?);
								"""	
						query_db(sql_str, (char_id, line, prev_amount + numberOfItems), False)

					
			except Exception as e:
				# Catch exception
				print(e)

	
		print(request.form)

	sql_str = """SELECT Item_Weight, Amount 
				FROM Inventory
				INNER JOIN Items ON Items.Item_ID = Inventory.Item_ID
				WHERE Character_ID=?;
				"""
	item_weights_query = query_db(sql_str, (char_id,), True)

	for item in item_weights_query:
		weight += float(item['Item_Weight']) * float(item['Amount'])

	print('weight: ' + str(weight))

	return str(weight)

@bp.route('/remove/items/<int:char_id>', methods=('GET', 'POST'))
@login_required
def remove_items(char_id):
	weight = 0

	if request.method == 'POST':
		if not check_if_user_has_character(session['user_id'], char_id):
			# TODO: change this to a exception later
			return 0
			#return '400

		print('request form: ')
		print(request.form)
	
		sql_str = """SELECT Amount, Items.Item_Weight
					FROM Inventory
					LEFT JOIN Items ON Items.Item_ID=Inventory.Item_ID
					WHERE Character_ID = ? AND Inventory.Item_ID = ?;
				"""
		try:
			for k in request.form:
				item_id = int(k)
				amount = int(request.form[k])
				print('item_id: ' + str(item_id))
				sql_str = """SELECT Amount
						FROM Inventory
						WHERE Character_ID = ? AND Item_ID = ?;
					"""

				item = query_db(sql_str, (char_id, item_id), True, True)

				new_amount = item['Amount'] - amount 

				if (new_amount) > 0:
					# update count
					sql_str = """UPDATE Inventory
								SET Amount = ?
								WHERE Item_ID = ? AND Character_ID = ?;
							"""
					query_db(sql_str, (new_amount, item_id, char_id), False)
				else:
					# check if equiped
					sql_str = """SELECT *
						FROM Character
						WHERE Character_ID = ?;
						"""
					characters = query_db(sql_str, (char_id,), True, True)

					item_id_list = [
						characters['Character_Head'], characters['Character_Shoulder'], characters['Character_Torso'],
						characters['Character_Hand'],characters['Character_Leg'],characters['Character_Foot'],
						characters['Character_Trinket1'], characters['Character_Trinket2'],characters['Character_Ring1'],
						characters['Character_Ring2'],characters['Character_Item1'],characters['Character_Item2'],
						characters['Character_Weapon1'], characters['Character_Weapon2'], characters['Character_Weapon3'],
						characters['Character_Weapon4']
					]

					isEquiped = False

					for iid in item_id_list:
						if iid == item_id:
							# is equiped
							isEquiped = True
							break

					if not isEquiped:
						# remove item
						sql_str = """DELETE FROM Inventory
									WHERE Item_ID = ? AND Character_ID = ?;
								"""
						query_db(sql_str, (item_id, char_id), False)
					else:
						print('unable to deleted a currently equiped item')

					
		except Exception as e:
			# Catch exception
			print(e)

	
		print(request.form)

	sql_str = """SELECT Item_Weight, Amount 
				FROM Inventory
				INNER JOIN Items ON Items.Item_ID = Inventory.Item_ID
				WHERE Character_ID=?;
				"""
	item_weights_query = query_db(sql_str, (char_id,), True)

	for item in item_weights_query:
		weight += float(item['Item_Weight']) * float(item['Amount'])

	print('weight: ' + str(weight))

	return str(weight)


@bp.route('item/equip/<int:char_id>/<int:item_id>/<int:slot_number>', methods=('GET', 'POST'))
@login_required
def item_equip(char_id, item_id, slot_number = 0):
	# Check for user_id associated with char_id
	sql_str = """SELECT *
				FROM Character
				WHERE Character.User_ID = ? AND Character.Character_ID = ?;
				"""

	characters = query_db(sql_str, (session['user_id'], char_id), True, True)

	if characters is None:
		# Error
		return redirect(url_for('character.character_select'))
	
	sql_str = """SELECT *
				FROM Inventory
				WHERE Character_ID = ? AND Item_ID = ?;
			"""
	item = query_db(sql_str, (char_id, item_id), True, True)
	if item is None:
		return redirect(url_for('character.character_select'))

	sql_str = """SELECT Slots.Slots_Name
			FROM Items
			INNER JOIN Slots ON Items.Item_Slot=Slots.Slots_ID
			WHERE Items.Item_ID = ?;
			"""

	slot_name = query_db(sql_str, (item_id,), True, True)['Slots_Name']

	modified_slot_name = slot_name

	if slot_number > 0 and slot_number < 4:
		modified_slot_name += str(slot_number)

	sql_str = """UPDATE Character 
			SET Character_""" + modified_slot_name + """=?
			WHERE Character_ID = ?;
			"""

	query_db(sql_str, (item_id, char_id,), False)

	sql_str = """SELECT *
				FROM Character
				WHERE Character.User_ID = ? AND Character.Character_ID = ?;
				"""

	characters = query_db(sql_str, (session['user_id'], char_id), True, True)

	sql_str = """SELECT Item_Picture, Item_Name, Rarities_Color
				FROM Items
				INNER JOIN Rarities ON Rarities.Rarities_ID=Items.Rarity_ID
				WHERE Item_ID = ?;
			"""
	item_data = query_db(sql_str, (item_id, ), True, True)

	item_data_dict = {
		'picture' : item_data['Item_Picture'],
		'name' : shorten_string(item_data['Item_Name'], 17),
		'color' : item_data['Rarities_Color']
	}


	item_id_list = [
		characters['Character_Head'], characters['Character_Shoulder'], characters['Character_Torso'],
		characters['Character_Hand'],characters['Character_Leg'],characters['Character_Foot'],
		 characters['Character_Trinket1'], characters['Character_Trinket2'],characters['Character_Ring1'],
		characters['Character_Ring2'],characters['Character_Item1'],characters['Character_Item2'],
		characters['Character_Weapon1'], characters['Character_Weapon2'], characters['Character_Weapon3'],
		characters['Character_Weapon4']
	] 


	stat_bonus = sumation_stats(item_id_list)

	character_data = {
		'max_hp' : convert_form_field_data_to_int(characters['Character_Max_HP']) + stat_bonus['health'],
		'ac' : convert_form_field_data_to_int(characters['Character_AC']) + stat_bonus['ac'],
		'initiative' : convert_form_field_data_to_int(characters['Character_Initiative']) + stat_bonus['initiative'],
		'attack_bonus' : convert_form_field_data_to_int(characters['Character_Attack_Bonus']) + stat_bonus['attack'],
		'weight' : convert_form_field_data_to_int(characters['Character_Base_Carrying_Cap']),
		#'max_weight' : convert_form_field_data_to_int(characters['Character_Max_Carry_Weight']),
		'max_weight' : 15 * (convert_form_field_data_to_int(characters['Character_Strength']) + stat_bonus['str']),
		'str' : convert_form_field_data_to_int(characters['Character_Strength']) + stat_bonus['str'],
		'dex' : convert_form_field_data_to_int(characters['Character_Dexterity']) + stat_bonus['dex'],
		'con' : convert_form_field_data_to_int(characters['Character_Constitution']) + stat_bonus['con'],
		'int' : convert_form_field_data_to_int(characters['Character_Intelligence']) + stat_bonus['int'],
		'wis' : convert_form_field_data_to_int(characters['Character_Wisdom']) + stat_bonus['wis'],
		'cha' : convert_form_field_data_to_int(characters['Character_Charisma']) + stat_bonus['cha'],
	}

	stat_modifiers = {
		'str_mod' :	calculate_modifier(character_data['str']), 
		'dex_mod' :	calculate_modifier(character_data['dex']),
		'con_mod' :	calculate_modifier(character_data['con']),
		'int_mod' :	calculate_modifier(character_data['int']),
		'wis_mod' :	calculate_modifier(character_data['wis']),
		'cha_mod' :	calculate_modifier(character_data['cha'])
	}
	return jsonify(
		character_data = character_data,
		stat_modifiers = stat_modifiers,
		slot_name = slot_name,
		modified_slot_name = modified_slot_name,
		item_data = item_data_dict
	)

@bp.route('item/unequip/<int:char_id>/<int:item_id>/<int:slot_number>', methods=('GET', 'POST'))
@login_required
def item_unequip(char_id, item_id, slot_number = 0):
	# Check for user_id associated with char_id
	sql_str = """SELECT *
				FROM Character
				WHERE Character.User_ID = ? AND Character.Character_ID = ?;
				"""

	characters = query_db(sql_str, (session['user_id'], char_id), True, True)

	if characters is None:
		# Error
		return redirect(url_for('character.character_select'))
	
	sql_str = """SELECT *
				FROM Inventory
				WHERE Character_ID = ? AND Item_ID = ?;
			"""
	item = query_db(sql_str, (char_id, item_id), True, True)
	if item is None:
		return redirect(url_for('character.character_select'))

	sql_str = """SELECT Slots.Slots_Name
			FROM Items
			INNER JOIN Slots ON Items.Item_Slot=Slots.Slots_ID
			WHERE Items.Item_ID = ?;
			"""

	slot_name = query_db(sql_str, (item_id,), True, True)['Slots_Name']

	modified_slot_name = slot_name

	if slot_number > 0 and slot_number < 5:
		modified_slot_name += str(slot_number)

	sql_str = """UPDATE Character 
			SET Character_""" + modified_slot_name + """=?
			WHERE Character_ID = ?;
			"""

	query_db(sql_str, (-1, char_id,), False)

	sql_str = """SELECT *
				FROM Character
				WHERE Character.User_ID = ? AND Character.Character_ID = ?;
				"""

	characters = query_db(sql_str, (session['user_id'], char_id), True, True)

	#item_data_dict = {
	#	'picture' : item_data['Item_Picture'],
	#	'name' : shorten_string(item_data['Item_Name'], 17),
	#	'color' : item_data['Rarities_Color']
	#}


	item_id_list = [
		characters['Character_Head'], characters['Character_Shoulder'], characters['Character_Torso'],
		characters['Character_Hand'],characters['Character_Leg'],characters['Character_Foot'],
		 characters['Character_Trinket1'], characters['Character_Trinket2'],characters['Character_Ring1'],
		characters['Character_Ring2'],characters['Character_Item1'],characters['Character_Item2'],
		characters['Character_Weapon1'], characters['Character_Weapon2'], characters['Character_Weapon3'],
		characters['Character_Weapon4']
	] 

	print(item_id_list)


	stat_bonus = sumation_stats(item_id_list)

	character_data = {
		'max_hp' : convert_form_field_data_to_int(characters['Character_Max_HP']) + stat_bonus['health'],
		'ac' : convert_form_field_data_to_int(characters['Character_AC']) + stat_bonus['ac'],
		'initiative' : convert_form_field_data_to_int(characters['Character_Initiative']) + stat_bonus['initiative'],
		'attack_bonus' : convert_form_field_data_to_int(characters['Character_Attack_Bonus']) + stat_bonus['attack'],
		'weight' : convert_form_field_data_to_int(characters['Character_Base_Carrying_Cap']),
		#'max_weight' : convert_form_field_data_to_int(characters['Character_Max_Carry_Weight']),
		'max_weight' : 15 * (convert_form_field_data_to_int(characters['Character_Strength']) + stat_bonus['str']),
		'str' : convert_form_field_data_to_int(characters['Character_Strength']) + stat_bonus['str'],
		'dex' : convert_form_field_data_to_int(characters['Character_Dexterity']) + stat_bonus['dex'],
		'con' : convert_form_field_data_to_int(characters['Character_Constitution']) + stat_bonus['con'],
		'int' : convert_form_field_data_to_int(characters['Character_Intelligence']) + stat_bonus['int'],
		'wis' : convert_form_field_data_to_int(characters['Character_Wisdom']) + stat_bonus['wis'],
		'cha' : convert_form_field_data_to_int(characters['Character_Charisma']) + stat_bonus['cha'],
	}

	stat_modifiers = {
		'str_mod' :	calculate_modifier(character_data['str']), 
		'dex_mod' :	calculate_modifier(character_data['dex']),
		'con_mod' :	calculate_modifier(character_data['con']),
		'int_mod' :	calculate_modifier(character_data['int']),
		'wis_mod' :	calculate_modifier(character_data['wis']),
		'cha_mod' :	calculate_modifier(character_data['cha'])
	}
	return jsonify(
		character_data = character_data,
		stat_modifiers = stat_modifiers,
		slot_name = slot_name,
		modified_slot_name = modified_slot_name,
		item_data = 'null'
 		#item_data = item_data_dict
	)