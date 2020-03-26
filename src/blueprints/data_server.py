import functools

import math

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, send_from_directory, current_app
)

from werkzeug.utils import secure_filename, escape

#from modules.data.database.db import get_db, query_db
from blueprints.auth import login_required

from logger.logger import Logger
from modules.data.database.query_modules import select_query 
from modules.data.database import data_helper

import os

bp = Blueprint('dataserver', __name__, url_prefix='/dataserver')

def _get_item_details(char_id, equipment_slot="", item_id=-1):
	# Get the character's item piece
	try:
		items = select_query.select_character_data(char_id, session['user_id'])
	except:
		Logger.error("ERROR: Items were not found")
		return ""

	if equipment_slot is not None and equipment_slot != "":
		try:
			item_id = items['Character_' + equipment_slot]
		except:
			Logger.error("ERROR: Items were not found")
			return ""

	# Ensure a proper item_id is given
	if item_id < 1:
		# TODO: needs better error handling
		raise Exception("Tried to get item details of item with id " + item_id)

	itemQueryResult = select_query.select_items(item_id) 

	# Check to see if ID has been assigned
	if itemQueryResult is None:
		itemQueryResult = data_helper.init_item_data() 

	#TODO: this effect query also shows up in admin.py... Could extract this to a function 
	if itemQueryResult is not None:
		# Check if item has an effect on it
		if itemQueryResult['Item_Effect1'] is not None and itemQueryResult['Item_Effect1'] > 0:	
			# Check to see if ID has been assigned
			effect1QueryResult = select_query.select_effect_data(itemQueryResult['Item_Effect1'])
		else:
			effect1QueryResult = {'Effect_Name' : 'Effect1', 'Effect_Description' : 'None'}

		# Check if item has an effect on it
		if itemQueryResult['Item_Effect2'] is not None and itemQueryResult['Item_Effect2'] > 0:	
			# Check to see if ID has been assigned
			effect2QueryResult = select_query.select_effect_data(itemQueryResult['Item_Effect2'])
		else:
			effect2QueryResult = {'Effect_Name' : 'Effect2', 'Effect_Description' : 'None'}

	image = url_for('static', filename='images/no_image.png')

	if itemQueryResult['Item_Picture'] is not None and itemQueryResult['Item_Picture'] != '' and itemQueryResult['Item_Picture'] != 'no_image.png':
		image = '/imageserver/item/' + itemQueryResult['Item_Picture']

	return data_helper.item_data_to_json(itemQueryResult, image, effect1QueryResult, effect2QueryResult)

# Equipment Data 
@bp.route('/equipmentItemDetails/<int:char_id>/<string:equipment_slot>', methods=('GET', 'POST'))
@login_required
def equipmentItemDetails(char_id, equipment_slot):
	# TODO: needs better error handling
	return _get_item_details(char_id, equipment_slot=equipment_slot)	

# Equipment Data 
@bp.route('/inventoryItemDetails/<int:char_id>/<int:item_id>', methods=('GET', 'POST'))
@login_required
def inventoryItemDetails(char_id, item_id):
	# TODO: needs better error handling
	return _get_item_details(char_id, item_id=item_id)	

@bp.route('getClassName/<int:char_id>')
@login_required
def get_class(char_id):
	query_result = select_query.select_character_class(session['user_id'], char_id)

	if query_result is None:
		return jsonify(current_value="Error getting Class Name")

	return jsonify(current_value=query_result["Class_Name"])

@bp.route('getRaceName/<int:char_id>')
@login_required
def get_race(char_id):
	query_result = select_query.select_character_race(session['user_id'], char_id)

	if query_result is None:
		return jsonify(current_value="Error getting Race Name")

	return jsonify(current_value=query_result["Race_Name"])

@bp.route('getAlignmentOptions')
@login_required
def get_alignment_options():
	alignments = select_query.get_alignments()

	alignment_name_and_id = []
	
	for item in alignments:
		alignment_name_and_id.append({'id' : item['Alignment_ID'], 'name' : item['Alignment_Name']})

	return jsonify(opts=alignment_name_and_id)

@bp.route('getLevel/<int:char_id>')
@login_required
def get_level(char_id):
	field_name = "Character_Level"
	query_result = select_query.select_char_fields(session['user_id'], char_id, (field_name,))

	if query_result is None:
		return jsonify(current_value=0)

	return jsonify(current_value=query_result[field_name])

@bp.route('getHealth/<int:char_id>')
@login_required
def get_health(char_id):
	field_name = "Character_HP"
	query_result = select_query.select_char_fields(session['user_id'], char_id, (field_name,))

	if query_result is None:
		return jsonify(current_value=0)

	return jsonify(current_value=query_result[field_name])

def get_stat_data(char_id : int, character_field : str, item_field : str):
	query_result = select_query.select_char_fields(session['user_id'], char_id, (character_field,))

	if query_result is None:
		return jsonify(current_value=0, base=0)

	base_stat = query_result[character_field]

	characters = select_query.select_character_data(char_id)

	item_id_list = data_helper.get_character_items_id(characters)

	stat_additional = 0

	for i in item_id_list:
		item = select_query.select_item_fields(i, (item_field,))
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
	field_name = "Character_Currency"
	query_result = select_query.select_char_fields(session['user_id'], char_id, (field_name,))

	if query_result is None:
		return jsonify(current_value=0)

	return jsonify(current_value=query_result[field_name])

@bp.route('dummyCall')
def dummy_call():
	return jsonify(response='I\'m a dummy')

@bp.route('getItemList/<int:item_slot>')
@login_required
def get_item_list(item_slot):
	field_names = ("Item_ID", "Item_Name", "Item_Picture", "Rarities_Color")
	query_result = select_query.select_item_fields_from_item_slot(item_slot, field_names)

	# TODO: handle if query_result is none

	item_list = []

	for item in query_result:
		item_data = {}
		for key in field_names:
			item_data[key] = item[key]

		item_list.append(item_data)

	slot_name = select_query.select_slot_names(item_slot)["Slots_Name"]

	output = {
		'slot_name' : slot_name,
		'items' : item_list
	}	

	return jsonify(output)

@bp.route('getCurrentEquipedItems/<int:char_id>/<int:item_slot>')
@login_required
def get_current_equiped_items(char_id, item_slot):
	characters = select_query.select_char_fields(session["user_id"], char_id)

	if characters is None:
		return redirect(url_for('character.character_select'))

	slot_name = select_query.select_slot_names(item_slot)["Slots_Name"]

	multiple = {'Weapon' : 4, 'Ring' : 2, 'Item' : 2, 'Trinket' : 2}

	r = 1
	slots = []

	if slot_name in multiple.keys():
		r = int(multiple[slot_name])
		for i in range(r):
			field_name = "Character_" + slot_name + str(i + 1)
			slots.append(field_name)
	else:
		slots.append("Character_" + slot_name)

	item_ids = select_query.select_char_fields(session["user_id"], char_id, tuple(slots))

	field_names = ['Item_ID', 'Item_Name', 'Item_Picture', 'Rarities_Color']

	item_list = []

	item_defaults = {
		'Ring' : {'item_name' : 'Ring', 'picture' : 'Ring.png'},
		'Item' : {'item_name' : 'Item',	'picture' : 'Item.png'},
		'Trinket' : {'item_name' : 'Trinket', 'picture' : 'Trinket.png'}
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
		join_str = "INNER JOIN Rarities ON Rarities.Rarities_ID=Items.Rarity_ID"
		item_data_result = select_query.select(tuple(field_names), "Items", False, "WHERE Item_ID=?", (i,), (join_str,))

		if item_data_result is None:
			count += 1
			continue

		temp_data = {}
		for name in field_names:
			temp_data[name] = item_data_result[name]
		
		item_list[count] = temp_data 
		count += 1

	slot_name = select_query.select_slot_names(item_slot)['Slots_Name']

	output = {'slot_name' : slot_name, 'items' : item_list, 'num_of_slots' : r}

	return jsonify(output)

@bp.route('getItemsInSlot/<int:char_id>/<string:item_slot>')
@login_required
def get_items_in_slot(char_id, item_slot):
	characters = select_query.select_char_fields(session["user_id"], char_id)
	if characters is None:
		return 'NULL'

	item_id_list = data_helper.get_character_items_id(characters)

	select_fields = (
		"Items.Item_ID", "Items.Item_Weight", "Items.Item_Name", "Rarities.Rarities_Color",
		"Slots.Slots_ID", "Inventory.Amount"
	)
	where_clause = "WHERE Inventory.Character_ID = ? AND Slots.Slots_Name = ?"
	joins = (
		"INNER JOIN Items on Inventory.Item_ID=Items.Item_ID",
		"INNER JOIN Rarities on Rarities.Rarities_ID=Items.Rarity_ID",
		"INNER JOIN Slots on Items.Item_Slot=Slots.Slots_ID"
	)
	query_result = select_query.select(select_fields, "Inventory", True, where_clause, (char_id, item_slot), joins)

	items = []	
	for q in query_result:
		
		item_fields = {
			'Item_ID' : q['Item_ID'],
			'Item_Weight' : q['Item_Weight'],
			'Item_Name' : escape(q['Item_Name']),
			'Rarities_Color' : q['Rarities_Color'],
			'Amount' : q['Amount'],
			'Slots_ID' : int(q['Slots_ID']),
			'Is_Equiped' : True if q['Item_ID'] in item_id_list else False
		}

		items.append(item_fields)

	return jsonify(items)

@bp.route('getItemAmount/<int:char_id>/<int:item_id>')
@login_required
def getItemAmount(char_id, item_id):
	characters = select_query.select_char_fields(session["user_id"], char_id)

	if characters is None:
		return redirect(url_for('character.character_select'))

	select_fields = ("Inventory.Item_ID", "Amount", "Items.Item_Slot", "Slots.Slots_Name")
	joins = (
		"LEFT JOIN Items ON Inventory.Item_ID = Items.Item_ID",
		"LEFT JOIN Slots ON Items.Item_Slot = Slots.Slots_ID"
	)
	where_clause = "WHERE Character_ID = ? AND Inventory.Item_ID = ?"
	query_result = select_query.select(select_fields, "Inventory", False, where_clause, (char_id, item_id), joins)

	return jsonify(
		current_value = query_result['Amount'],
		item_id = query_result['Item_ID'],
		slot_name = query_result['Slots_Name']
	)



@bp.route('/itemDetails/<int:item_id>')
@login_required
def getItemDetails(item_id):
	select_fields = ("Item_Name", "Item_Picture", "Rarities.Rarities_Color")
	joins = ("INNER JOIN Rarities ON Rarities.Rarities_ID=Items.Rarity_ID",)
	where_clause = "WHERE Item_ID = ?"
	result = select_query.select(select_fields, "Items", False, where_clause, (item_id,), joins)

	return jsonify(
		name=result['Item_name'],
		picture=result['Item_Picture'],
		color=result['Rarities_Color']
	)