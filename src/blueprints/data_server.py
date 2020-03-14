import functools

import math

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, send_from_directory, current_app
)

from werkzeug.utils import secure_filename, escape

from modules.data.database.db import get_db, query_db
from blueprints.auth import login_required

import os

bp = Blueprint('dataserver', __name__, url_prefix='/dataserver')

# Equipment Data 
@bp.route('/equipmentItemDetails/<int:char_id>/<string:equipment_slot>', methods=('GET', 'POST'))
@login_required
def equipmentItemDetails(char_id, equipment_slot):
	# Get the character's item piece
	queryStr = """SELECT * 
				FROM Character
				WHERE Character_ID=? AND User_ID=?;
				"""
	try:
		items = query_db(queryStr, (char_id, session['user_id'],), True, True)
	except:
		print("ERROR: Items were not found")
		return ""

	try:
		print(items)
		item_id = items['Character_' + equipment_slot]
	except:
		print("ERROR: Item was not found")
		return ""

	# Items query
	queryStr = """SELECT *
				FROM Items
				LEFT JOIN Rarities ON Items.Rarity_ID=Rarities.Rarities_ID
				WHERE Items.Item_ID=?;"""
	# Check to see if ID has been assigned
	
	itemQueryResult = query_db(queryStr, (item_id,), True, True)

	if itemQueryResult is None:
		itemQueryResult = {
			'Item_Description' : 'null',
			'Item_Name' : 'null',
			'Item_Picture' : 'no_image.png',
			'Rarities_Name' : 'null',
			'Rarities_Color' : 'white',
			'Item_Slot' : 'null',
			'Item_Weight' : 'null',
			'Item_Str_Bonus' : 0,
			'Item_Dex_Bonus' : 0,
			'Item_Con_Bonus' : 0,
			'Item_Int_Bonus' : 0,
			'Item_Wis_Bonus' : 0,
			'Item_Cha_Bonus' : 0,
			'Item_Effect1' : None,
			'Item_Effect2' : None,
			'Item_Damage_Num_Of_Dices' : 0,
			'Item_Damage_Num_Of_Dice_Sides' : 0,
			'Item_AC_Bonus' : 0,
			'Item_Bonus_Attack' : 0,
			'Wield_Str' : 0,
			'Wield_Dex' : 0,
			'Wield_Wis' : 0,
			'Wield_Int' : 0
		}

	# Check if item has an effect on it
	if itemQueryResult is not None and itemQueryResult['Item_Effect1'] is not None and itemQueryResult['Item_Effect1'] > 0:	
		# Effect1 query
		queryStr = """SELECT *
					FROM Effects 
					WHERE Effect_ID=?;"""
		# Check to see if ID has been assigned
		
		effect1QueryResult = query_db(queryStr, (itemQueryResult['Item_Effect1'],), True, True)
	else:
		effect1QueryResult = {'Effect_Name' : 'Effect1', 'Effect_Description' : 'None'}

	# Check if item has an effect on it
	if itemQueryResult is not None and itemQueryResult['Item_Effect2'] is not None and itemQueryResult['Item_Effect2'] > 0:	
		# Effect2 query
		queryStr = """SELECT *
					FROM Effects 
					WHERE Effect_ID=?;"""
		# Check to see if ID has been assigned
		
		effect2QueryResult = query_db(queryStr, (itemQueryResult['Item_Effect2'],), True, True)
	else:
		effect2QueryResult = {'Effect_Name' : 'Effect2', 'Effect_Description' : 'None'}

	image = url_for('static', filename='images/no_image.png')

	if itemQueryResult['Item_Picture'] is not None and itemQueryResult['Item_Picture'] != '' and itemQueryResult['Item_Picture'] != 'no_image.png':
		image = '/imageserver/item/' + itemQueryResult['Item_Picture']

	return jsonify(
		description=itemQueryResult['Item_Description'],
		name=itemQueryResult['Item_Name'],
		image=image,
		rarity=itemQueryResult['Rarities_Name'],
		rarity_color=itemQueryResult['Rarities_Color'],
		slot=itemQueryResult['Item_Slot'],
		weight=itemQueryResult['Item_Weight'],
		str_bonus=itemQueryResult['Item_Str_Bonus'],
		dex_bonus=itemQueryResult['Item_Dex_Bonus'],
		con_bonus=itemQueryResult['Item_Con_Bonus'],
		int_bonus=itemQueryResult['Item_Int_Bonus'],
		wis_bonus=itemQueryResult['Item_Wis_Bonus'],
		cha_bonus=itemQueryResult['Item_Cha_Bonus'],
		effect1_name=effect1QueryResult['Effect_Name'],
		effect1_description=effect1QueryResult['Effect_Description'],
		effect2_name=effect2QueryResult['Effect_Name'],
		effect2_description=effect2QueryResult['Effect_Description'],
		item_damage_num_of_dices=itemQueryResult['Item_Damage_Num_Of_Dices'],
		item_damage_num_of_dice_sides=itemQueryResult['Item_Damage_Num_Of_Dice_Sides'],
		ac=itemQueryResult['Item_AC_Bonus'],
		bonus_damage=itemQueryResult['Item_Bonus_Attack'],
		wield_str=itemQueryResult['Wield_Str'],
		wield_dex=itemQueryResult['Wield_Dex'],
		wield_wis=itemQueryResult['Wield_Wis'],
		wield_int=itemQueryResult['Wield_Int'],
	)


# Equipment Data 
@bp.route('/inventoryItemDetails/<int:char_id>/<int:item_id>', methods=('GET', 'POST'))
@login_required
def inventoryItemDetails(char_id, item_id):
	sql_str = """SELECT *
				FROM Character
				WHERE Character.User_ID = ? AND Character.Character_ID = ?;
				"""

	characters = query_db(sql_str, (session['user_id'], char_id), True, True)

	if characters is None:
		# Error
		return redirect(url_for('character.character_select'))
	# Get the character's item piece
	queryStr = """SELECT * 
				FROM Inventory 
				WHERE Character_ID=? AND Item_ID=?;
				"""
	try:
		items = query_db(queryStr, (char_id, item_id), True, True)
		item_id = items['Item_ID']
	except:
		print("ERROR: Item was not found")
		return ""

	# Items query
	queryStr = """SELECT *
				FROM Items
				LEFT JOIN Rarities ON Items.Rarity_ID=Rarities.Rarities_ID
				WHERE Items.Item_ID=?;"""
	# Check to see if ID has been assigned
	
	itemQueryResult = query_db(queryStr, (item_id,), True, True)

	if itemQueryResult is None:
		itemQueryResult = {
			'Item_Description' : 'null',
			'Item_Name' : 'null',
			'Item_Picture' : 'no_image.png',
			'Rarities_Name' : 'null',
			'Rarities_Color' : 'white',
			'Item_Slot' : 'null',
			'Item_Weight' : 'null',
			'Item_Str_Bonus' : 0,
			'Item_Dex_Bonus' : 0,
			'Item_Con_Bonus' : 0,
			'Item_Int_Bonus' : 0,
			'Item_Wis_Bonus' : 0,
			'Item_Cha_Bonus' : 0,
			'Item_Effect1' : None,
			'Item_Effect2' : None,
			'Item_Damage_Num_Of_Dices' : 0,
			'Item_Damage_Num_Of_Dice_Sides' : 0,
			'Item_AC_Bonus' : 0,
			'Item_Bonus_Attack' : 0,
			'Wield_Str' : 0,
			'Wield_Dex' : 0,
			'Wield_Wis' : 0,
			'Wield_Int' : 0
		}

	# Check if item has an effect on it
	if itemQueryResult is not None and itemQueryResult['Item_Effect1'] is not None and itemQueryResult['Item_Effect1'] > 0:	
		# Effect1 query
		queryStr = """SELECT *
					FROM Effects 
					WHERE Effect_ID=?;"""
		# Check to see if ID has been assigned
		
		effect1QueryResult = query_db(queryStr, (itemQueryResult['Item_Effect1'],), True, True)
	else:
		effect1QueryResult = {'Effect_Name' : 'Effect1', 'Effect_Description' : 'None'}

	# Check if item has an effect on it
	if itemQueryResult is not None and itemQueryResult['Item_Effect2'] is not None and itemQueryResult['Item_Effect2'] > 0:	
		# Effect2 query
		queryStr = """SELECT *
					FROM Effects 
					WHERE Effect_ID=?;"""
		# Check to see if ID has been assigned
		
		effect2QueryResult = query_db(queryStr, (itemQueryResult['Item_Effect2'],), True, True)
	else:
		effect2QueryResult = {'Effect_Name' : 'Effect2', 'Effect_Description' : 'None'}

	image = url_for('static', filename='images/no_image.png')

	if itemQueryResult['Item_Picture'] is not None and itemQueryResult['Item_Picture'] != '' and itemQueryResult['Item_Picture'] != 'no_image.png':
		image = '/imageserver/item/' + itemQueryResult['Item_Picture']

	return jsonify(
		description=itemQueryResult['Item_Description'],
		name=itemQueryResult['Item_Name'],
		image=image,
		rarity=itemQueryResult['Rarities_Name'],
		rarity_color=itemQueryResult['Rarities_Color'],
		slot=itemQueryResult['Item_Slot'],
		weight=itemQueryResult['Item_Weight'],
		str_bonus=itemQueryResult['Item_Str_Bonus'],
		dex_bonus=itemQueryResult['Item_Dex_Bonus'],
		con_bonus=itemQueryResult['Item_Con_Bonus'],
		int_bonus=itemQueryResult['Item_Int_Bonus'],
		wis_bonus=itemQueryResult['Item_Wis_Bonus'],
		cha_bonus=itemQueryResult['Item_Cha_Bonus'],
		effect1_name=effect1QueryResult['Effect_Name'],
		effect1_description=effect1QueryResult['Effect_Description'],
		effect2_name=effect2QueryResult['Effect_Name'],
		effect2_description=effect2QueryResult['Effect_Description'],
		item_damage_num_of_dices=itemQueryResult['Item_Damage_Num_Of_Dices'],
		item_damage_num_of_dice_sides=itemQueryResult['Item_Damage_Num_Of_Dice_Sides'],
		ac=itemQueryResult['Item_AC_Bonus'],
		bonus_damage=itemQueryResult['Item_Bonus_Attack'],
		wield_str=itemQueryResult['Wield_Str'],
		wield_dex=itemQueryResult['Wield_Dex'],
		wield_wis=itemQueryResult['Wield_Wis'],
		wield_int=itemQueryResult['Wield_Int'],
	)

@bp.route('/characterInfo/<int:char_id>/<string:field>', methods=('GET', 'POST'))
@login_required
def character_info_field(char_id, field):
	# Get the character's item piece
	queryStr = """SELECT * 
				FROM Character
				WHERE Character_ID=? AND User_ID=?;
				"""
	try:
		items = query_db(queryStr, (char_id, session['user_id'],), True, True)
	except:
		print("ERROR: Items were not found")
		return ""

	try:
		item_id = items['Character_' + equipment_slot]
	except:
		print("ERROR: Item was not found")
		return ""

	# Items query
	queryStr = """SELECT *
				FROM Items
				LEFT JOIN Rarities ON Items.Rarity_ID=Rarities.Rarities_ID
				WHERE Items.Item_ID=?;"""
	# Check to see if ID has been assigned
	return

#@bp.route('/images/<string:image>', methods=('GET', 'POST'))
#@login_required
#def get_image(image):
#	converted_image = convert_image_to_base64(os.path.join(current_app.config['IMAGE_UPLOAD'], secure_filename(image))) 
#	return 'hello <img src="data:image/jpg;charset=utf-8;base64, ' + str(converted_image['encoded_image']) + '" />'
#	#return str(converted_image['encoded_image'])


@bp.route('getClassOptions')
@login_required
def get_class_options():
	sql_str = """SELECT Class_ID, Class_Name
			FROM Class;
			"""
	class_data = query_db(sql_str)

	class_name_and_id = []
	
	for item in class_data:
		class_name_and_id.append({'id' : item['Class_ID'], 'name' : item['Class_Name']})

	return jsonify(classes=class_name_and_id)

@bp.route('getClassName/<int:char_id>')
@login_required
def get_class(char_id):
	sql_str = """SELECT Class_Name 
			FROM Character
			INNER JOIN Class ON Class.Class_ID = Character.Character_Class
			WHERE User_ID = ? AND Character_ID = ?;
			"""
	query_result = query_db(sql_str, (session['user_id'], char_id), True, True)

	if query_result is None:
		return jsonify(current_value="Error getting Class Name")

	return jsonify(current_value=query_result["Class_Name"])


@bp.route('getRaceName/<int:char_id>')
@login_required
def get_race(char_id):
	sql_str = """SELECT Race_Name 
			FROM Character
			INNER JOIN Races ON Races.Race_ID = Character.Character_Race
			WHERE User_ID = ? AND Character_ID = ?;
			"""
	query_result = query_db(sql_str, (session['user_id'], char_id), True, True)

	if query_result is None:
		return jsonify(current_value="Error getting Race Name")

	return jsonify(current_value=query_result["Race_Name"])


@bp.route('getAlignmentOptions')
@login_required
def get_alignment_options():
	sql_str = """SELECT Alignment_ID, Alignment_Name
			FROM Alignments;
			"""
	class_data = query_db(sql_str)

	class_name_and_id = []
	
	for item in class_data:
		class_name_and_id.append({'id' : item['Alignment_ID'], 'name' : item['Alignment_Name']})

	return jsonify(classes=class_name_and_id)

@bp.route('getLevel/<int:char_id>')
@login_required
def get_level(char_id):
	sql_str = """SELECT Character_Level
			FROM Character
			WHERE User_ID = ? AND Character_ID = ?;
			"""
	query_result = query_db(sql_str, (session['user_id'], char_id), True, True)

	if query_result is None:
		return jsonify(current_value=0)

	return jsonify(current_value=query_result['Character_Level'])

@bp.route('getHealth/<int:char_id>')
@login_required
def get_health(char_id):
	sql_str = """SELECT Character_HP
			FROM Character
			WHERE User_ID = ? AND Character_ID = ?;
			"""
	query_result = query_db(sql_str, (session['user_id'], char_id), True, True)

	if query_result is None:
		return jsonify(current_value=0)

	return jsonify(current_value=query_result['Character_HP'])

def get_stat_data(char_id : int, character_field : str, item_field : str):
	sql_str = """SELECT """ + character_field + """
			FROM Character
			WHERE User_ID = ? AND Character_ID = ?;
			"""
	query_result = query_db(sql_str, (session['user_id'], char_id), True, True)

	if query_result is None:
		return jsonify(current_value=0, base=0)

	base_stat = query_result[character_field]

	

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


	return jsonify(additional=stat_additional, base=base_stat)

@bp.route('getMaxHealth/<int:char_id>')
@login_required
def get_max_health(char_id):
	return get_stat_data(char_id, 'Character_Max_HP', 'Item_Health_Bonus')

@bp.route('getAC/<int:char_id>')
@login_required
def get_AC(char_id):
	return get_stat_data(char_id, 'Character_AC', 'Item_AC_Bonus')

@bp.route('getInitiative/<int:char_id>')
@login_required
def get_initiative(char_id):
	return get_stat_data(char_id, 'Character_Initiative', 'Item_Initiative_Bonus')
	
@bp.route('getAttackBonus/<int:char_id>')
@login_required
def get_attack_bonus(char_id):
	return get_stat_data(char_id, 'Character_Attack_Bonus', 'Item_Attack_Bonus')

@bp.route('getStr/<int:char_id>')
@login_required
def get_str(char_id):
	return get_stat_data(char_id, 'Character_Strength', 'Item_Str_Bonus')

@bp.route('getDex/<int:char_id>')
@login_required
def get_dex(char_id):
	return get_stat_data(char_id, 'Character_Dexterity', 'Item_Dex_Bonus')

@bp.route('getCon/<int:char_id>')
@login_required
def get_con(char_id):
	return get_stat_data(char_id, 'Character_Constitution', 'Item_Con_Bonus')

@bp.route('getInt/<int:char_id>')
@login_required
def get_int(char_id):
	return get_stat_data(char_id, 'Character_Intelligence', 'Item_Int_Bonus')

@bp.route('getWis/<int:char_id>')
@login_required
def get_wis(char_id):
	return get_stat_data(char_id, 'Character_Wisdom', 'Item_Wis_Bonus')

@bp.route('getCha/<int:char_id>')
@login_required
def get_cha(char_id):
	return get_stat_data(char_id, 'Character_Charisma', 'Item_Cha_Bonus')

@bp.route('getCurrency/<int:char_id>')
@login_required
def get_currency(char_id):
	sql_str = """SELECT Character_Currency
			FROM Character
			WHERE User_ID = ? AND Character_ID = ?;
			"""
	query_result = query_db(sql_str, (session['user_id'], char_id), True, True)

	if query_result is None:
		return jsonify(current_value=0)

	return jsonify(current_value=query_result['Character_Currency'])

@bp.route('dummyCall')
def dummy_call():
	return jsonify(response='I\'m a dummy')


@bp.route('getItemList/<int:item_slot>')
@login_required
def get_item_list(item_slot):
	field_names = [
		'Item_ID',
		'Item_Name',
		'Item_Picture',
		'Rarities_Color'
	]

	sql_str = """SELECT """

	for name in field_names:
		sql_str += name
		if name != field_names[-1]:
			sql_str += ','
		
		sql_str += ' '

	sql_str += """\nFROM Items
			INNER JOIN Rarities ON Rarities.Rarities_ID=Items.Rarity_ID
			WHERE Item_Slot = ?;
			"""

	query_result = query_db(sql_str, (item_slot,), True)

	item_list = []

	for item in query_result:
		item_data = {}
		for key in field_names:
			item_data[key] = item[key]

		item_list.append(item_data)

	sql_str = """SELECT Slots_Name
			FROM SLOTS
			WHERE Slots_ID = ?;
			"""
	slot_name = query_db(sql_str, (item_slot,), True, True)['Slots_Name']

	output = {
		'slot_name' : slot_name,
		'items' : item_list
	}	

	return jsonify(output)

@bp.route('getCurrentEquipedItems/<int:char_id>/<int:item_slot>')
@login_required
def get_current_equiped_items(char_id, item_slot):
	sql_str = """SELECT *
				FROM Character
				WHERE Character.User_ID = ? AND Character.Character_ID = ?;
				"""

	characters = query_db(sql_str, (session['user_id'], char_id), True, True)

	if characters is None:
		# Error
		return redirect(url_for('character.character_select'))

	sql_str = """SELECT Slots_Name
				FROM Slots
				WHERE Slots_ID = ?;
			"""	
	slot_name = query_db(sql_str, (item_slot,), True, True)['Slots_Name']

	multiple = {
		'Weapon' : 4,
		'Ring' : 2,
		'Item' : 2,
		'Trinket' : 2
	}

	sql_str = """SELECT """

	r = 1

	slots = []

	if slot_name in multiple.keys():
		r = int(multiple[slot_name])
		for i in range(r):
			field_name = "Character_" + slot_name + str(i + 1)
			slots.append(field_name)
			sql_str += field_name

			if i < r - 1:
				sql_str += ", "
			else:
				sql_str += "\n"
	else:
		sql_str +=  "Character_" + slot_name + "\n"

	sql_str += """FROM Character
			WHERE Character_ID = ?;
			"""

	item_ids = query_db(sql_str, (char_id,), True, True)

	field_names = [
		'Item_ID',
		'Item_Name',
		'Item_Picture',
		'Rarities_Color'
	]

	sql_str = """SELECT """

	for name in field_names:
		sql_str += name
		if name != field_names[-1]:
			sql_str += ','
		
		sql_str += ' '

	temp = 0

	item_list = []

	item_defaults = {
		'Ring' : {
			'item_name' : 'Ring',
			'picture' : 'Ring.png'
		},
		'Item' : {
			'item_name' : 'Item',
			'picture' : 'Item.png'
		},
		'Trinket' : {
			'item_name' : 'Trinket',
			'picture' : 'Trinket.png'
		}
	}

	for i in range(r):
		temp_dict = {}

		temp_dict['Item_ID'] = -1



		if slot_name == 'Weapon':
			if i % 2 == 1:
				temp_dict['Item_Name'] = 'Off Hand '
				temp_dict['Item_Picture'] = 'Off_Hand.png'
			else:
				temp_dict['Item_Name'] = 'Main Hand '
				temp_dict['Item_Picture'] = 'Main_Hand.png'
			temp_dict['Item_Name'] += str(math.ceil((i + 1) / 2))
		else:
			temp_dict['Item_Name'] = item_defaults[slot_name]['item_name']
			temp_dict['Item_Picture'] = item_defaults[slot_name]['picture']

		temp_dict['Rarities_Color'] = '#606060'


		item_list.append(temp_dict)

	count = 0
	for i in item_ids:
		sql_str = """SELECT Item_ID, Item_Name, Item_Picture, Rarities.Rarities_Color
					FROM Items
					INNER JOIN Rarities ON Rarities.Rarities_ID=Items.Rarity_ID
					WHERE Item_ID = ?;
				"""
		item_data_result = query_db(sql_str, (i,), True, True)
		if item_data_result is None:
			count += 1
			continue	
		#item_data_result['internal_slot_num'] = 
		temp_data = {}
		for name in field_names:
			print('item_data_result[' + name + ']: ' + str(item_data_result[name]))
			temp_data[name] = item_data_result[name]
		
		item_list[count] = temp_data 
		count += 1
		


	sql_str = """SELECT Slots_Name
			FROM SLOTS
			WHERE Slots_ID = ?;
			"""
	slot_name = query_db(sql_str, (item_slot,), True, True)['Slots_Name']

	output = {
		'slot_name' : slot_name,
		'items' : item_list,
		'num_of_slots' : r
	}	


	return jsonify(output)

@bp.route('getItemsInSlot/<int:char_id>/<string:item_slot>')
@login_required
def get_items_in_slot(char_id, item_slot):
	sql_str = """SELECT * 
			FROM Character
			WHERE User_ID = ? AND Character_ID = ?;
			"""
	characters = query_db(sql_str, (session['user_id'], char_id), True, True)
	if characters is None:
		return 'NULL'

	items = []	

	item_id_list = [
		characters['Character_Head'], characters['Character_Shoulder'], characters['Character_Torso'],
		characters['Character_Hand'],characters['Character_Leg'],characters['Character_Foot'],
		 characters['Character_Trinket1'], characters['Character_Trinket2'],characters['Character_Ring1'],
		characters['Character_Ring2'],characters['Character_Item1'],characters['Character_Item2'],
		characters['Character_Weapon1'], characters['Character_Weapon2'], characters['Character_Weapon3'],
		characters['Character_Weapon4']
	] 
	
	sql_str = """SELECT Items.Item_ID, Items.Item_Weight, Items.Item_Name, Rarities.Rarities_Color, Slots.Slots_ID, Inventory.Amount
				FROM Inventory
				INNER JOIN Items on Inventory.Item_ID=Items.Item_ID
				INNER JOIN Rarities on Rarities.Rarities_ID=Items.Rarity_ID
				INNER JOIN Slots on Items.Item_Slot=Slots.Slots_ID
				WHERE Inventory.Character_ID = ? AND Slots.Slots_Name = ?;
			"""
	query_result = query_db(sql_str, (char_id, item_slot), True)

	for q in query_result:
		
		item_fields = {
			'Item_ID' : q['Item_ID'],
			'Item_Weight' : q['Item_Weight'],
			'Item_Name' : escape(q['Item_Name']),
			'Rarities_Color' : q['Rarities_Color'],
			'Amount' : q['Amount'],
			#'Slots_Name' : q['Slots_Name'],
			'Slots_ID' : int(q['Slots_ID']),
			'Is_Equiped' : True if q['Item_ID'] in item_id_list else False
		}

		items.append(item_fields)

	print(items)

	return jsonify(items)

@bp.route('getItemAmount/<int:char_id>/<int:item_id>')
@login_required
def getItemAmount(char_id, item_id):
	sql_str = """SELECT *
				FROM Character
				WHERE Character.User_ID = ? AND Character.Character_ID = ?;
				"""

	characters = query_db(sql_str, (session['user_id'], char_id), True, True)

	if characters is None:
		# Error
		return redirect(url_for('character.character_select'))


	sql_str = """SELECT Inventory.Item_ID, Amount, Items.Item_Slot, Slots.Slots_Name
			FROM Inventory
			LEFT JOIN Items ON Inventory.Item_ID = Items.Item_ID
			LEFT JOIN Slots ON Items.Item_Slot = Slots.Slots_ID
			WHERE Character_ID = ? AND Inventory.Item_ID = ?;
			"""
	query_result = query_db(sql_str, (char_id, item_id), True, True)


	return jsonify(
		current_value = query_result['Amount'],
		item_id = query_result['Item_ID'],
		slot_name = query_result['Slots_Name']
	)



@bp.route('/itemDetails/<int:item_id>')
@login_required
def getItemDetails(item_id):
	sql_str = """SELECT Item_Name, Item_Picture, Rarities.Rarities_Color
				FROM Items
				INNER JOIN Rarities ON Rarities.Rarities_ID=Items.Rarity_ID
				WHERE Item_ID = ?;
			"""
	result = query_db(sql_str, (item_id, ), True, True)

	return jsonify(
		name=result['Item_name'],
		picture=result['Item_Picture'],
		color=result['Rarities_Color']
	)