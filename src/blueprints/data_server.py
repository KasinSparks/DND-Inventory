import functools

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, send_from_directory, current_app
)

from ..image_sever import convert_image_to_base64

from werkzeug import secure_filename

from ..db import get_db, query_db
from .auth import login_required

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
		itemQueryResult = {'Item_Description' : 'null',
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
							'Item_Effect2' : None
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
		image = '/dataserver/imageserver/item/' + itemQueryResult['Item_Picture']

	return jsonify(description=itemQueryResult['Item_Description'],
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

@bp.route('getMaxHealth/<int:char_id>')
@login_required
def get_max_health(char_id):
	sql_str = """SELECT Character_Max_HP
			FROM Character
			WHERE User_ID = ? AND Character_ID = ?;
			"""
	query_result = query_db(sql_str, (session['user_id'], char_id), True, True)

	if query_result is None:
		return jsonify(current_value=0, base=0)

	base_max_hp = query_result['Character_Max_HP']

	

	sql_str = """SELECT *
			FROM Character
			WHERE Character_ID = ?;
			"""
	characters = query_db(sql_str, (char_id,), True, True)

	item_id_list = [
		characters['Character_Helmet'], characters['Character_Shoulders'], characters['Character_Chest'],
		characters['Character_Gloves'],characters['Character_Leggings'],characters['Character_Boots'],
		 characters['Character_Trinket1'], characters['Character_Trinket2'],characters['Character_Ring1'],
		characters['Character_Ring2'],characters['Character_Magic_Item1'],characters['Character_Magic_Item2'],
		characters['Character_Weapon1'], characters['Character_Weapon2'], characters['Character_Weapon3'],
		characters['Character_Weapon4']
	]

	health_additional = 0

	for i in item_id_list:
		sql_str = """SELECT Item_Health_Bonus
				FROM Items
				WHERE Item_ID = ?;
				""" 
		item = query_db(sql_str, (i,), True, True)
		if item is not None:
			health_additional += item['Item_Health_Bonus']


	return jsonify(additional=health_additional, base=base_max_hp)

@bp.route('getAC/<int:char_id>')
@login_required
def get_AC(char_id):
	sql_str = """SELECT Character_AC
			FROM Character
			WHERE User_ID = ? AND Character_ID = ?;
			"""
	query_result = query_db(sql_str, (session['user_id'], char_id), True, True)

	if query_result is None:
		return jsonify(current_value=0, base=0)

	base_ac = query_result['Character_AC']

	

	sql_str = """SELECT *
			FROM Character
			WHERE Character_ID = ?;
			"""
	characters = query_db(sql_str, (char_id,), True, True)

	item_id_list = [
		characters['Character_Helmet'], characters['Character_Shoulders'], characters['Character_Chest'],
		characters['Character_Gloves'],characters['Character_Leggings'],characters['Character_Boots'],
		 characters['Character_Trinket1'], characters['Character_Trinket2'],characters['Character_Ring1'],
		characters['Character_Ring2'],characters['Character_Magic_Item1'],characters['Character_Magic_Item2'],
		characters['Character_Weapon1'], characters['Character_Weapon2'], characters['Character_Weapon3'],
		characters['Character_Weapon4']
	]

	ac_additional = 0

	for i in item_id_list:
		sql_str = """SELECT Item_AC_Bonus
				FROM Items
				WHERE Item_ID = ?;
				""" 
		item = query_db(sql_str, (i,), True, True)
		if item is not None:
			ac_additional += item['Item_AC_Bonus']


	return jsonify(additional=ac_additional, base=base_ac)

@bp.route('getInitiative/<int:char_id>')
@login_required
def get_initiative(char_id):
	sql_str = """SELECT Character_Initiative
			FROM Character
			WHERE User_ID = ? AND Character_ID = ?;
			"""
	query_result = query_db(sql_str, (session['user_id'], char_id), True, True)

	if query_result is None:
		return jsonify(current_value=0, base=0)

	base_initiative = query_result['Character_Initiative']

	

	sql_str = """SELECT *
			FROM Character
			WHERE Character_ID = ?;
			"""
	characters = query_db(sql_str, (char_id,), True, True)

	item_id_list = [
		characters['Character_Helmet'], characters['Character_Shoulders'], characters['Character_Chest'],
		characters['Character_Gloves'],characters['Character_Leggings'],characters['Character_Boots'],
		 characters['Character_Trinket1'], characters['Character_Trinket2'],characters['Character_Ring1'],
		characters['Character_Ring2'],characters['Character_Magic_Item1'],characters['Character_Magic_Item2'],
		characters['Character_Weapon1'], characters['Character_Weapon2'], characters['Character_Weapon3'],
		characters['Character_Weapon4']
	]

	initiative_additional = 0

	for i in item_id_list:
		sql_str = """SELECT Item_Initiative_Bonus
				FROM Items
				WHERE Item_ID = ?;
				""" 
		item = query_db(sql_str, (i,), True, True)
		if item is not None:
			initiative_additional += item['Item_Initiative_Bonus']


	return jsonify(additional=initiative_additional, base=base_initiative)

@bp.route('getAttackBonus/<int:char_id>')
@login_required
def get_attack_bonus(char_id):
	sql_str = """SELECT Character_Attack_Bonus
			FROM Character
			WHERE User_ID = ? AND Character_ID = ?;
			"""
	query_result = query_db(sql_str, (session['user_id'], char_id), True, True)

	if query_result is None:
		return jsonify(current_value=0, base=0)

	base_stat = query_result['Character_Attack_Bonus']

	

	sql_str = """SELECT *
			FROM Character
			WHERE Character_ID = ?;
			"""
	characters = query_db(sql_str, (char_id,), True, True)

	item_id_list = [
		characters['Character_Helmet'], characters['Character_Shoulders'], characters['Character_Chest'],
		characters['Character_Gloves'],characters['Character_Leggings'],characters['Character_Boots'],
		 characters['Character_Trinket1'], characters['Character_Trinket2'],characters['Character_Ring1'],
		characters['Character_Ring2'],characters['Character_Magic_Item1'],characters['Character_Magic_Item2'],
		characters['Character_Weapon1'], characters['Character_Weapon2'], characters['Character_Weapon3'],
		characters['Character_Weapon4']
	]

	stat_additional = 0

	for i in item_id_list:
		sql_str = """SELECT Item_Attack_Bonus
				FROM Items
				WHERE Item_ID = ?;
				""" 
		item = query_db(sql_str, (i,), True, True)
		if item is not None:
			stat_additional += item['Item_Attack_Bonus']


	return jsonify(additional=stat_additional, base=base_stat)


@bp.route('getStr/<int:char_id>')
@login_required
def get_str(char_id):
	sql_str = """SELECT Character_Strength
			FROM Character
			WHERE User_ID = ? AND Character_ID = ?;
			"""
	query_result = query_db(sql_str, (session['user_id'], char_id), True, True)

	if query_result is None:
		return jsonify(current_value=0, base=0)

	base_stat = query_result['Character_Strength']

	

	sql_str = """SELECT *
			FROM Character
			WHERE Character_ID = ?;
			"""
	characters = query_db(sql_str, (char_id,), True, True)

	item_id_list = [
		characters['Character_Helmet'], characters['Character_Shoulders'], characters['Character_Chest'],
		characters['Character_Gloves'],characters['Character_Leggings'],characters['Character_Boots'],
		 characters['Character_Trinket1'], characters['Character_Trinket2'],characters['Character_Ring1'],
		characters['Character_Ring2'],characters['Character_Magic_Item1'],characters['Character_Magic_Item2'],
		characters['Character_Weapon1'], characters['Character_Weapon2'], characters['Character_Weapon3'],
		characters['Character_Weapon4']
	]

	stat_additional = 0

	for i in item_id_list:
		sql_str = """SELECT Item_Str_Bonus
				FROM Items
				WHERE Item_ID = ?;
				""" 
		item = query_db(sql_str, (i,), True, True)
		if item is not None:
			stat_additional += item['Item_Str_Bonus']


	return jsonify(additional=stat_additional, base=base_stat)

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

@bp.route('/imageserver/user/<string:image_name>')
@login_required
def getUserImage(image_name):
	# TODO: Read the docs on how to improve this for server
	
	return send_from_directory(os.path.join('..', current_app.config['IMAGE_UPLOAD'], 'users', str(session['user_id'])), image_name, as_attachment=False)
	
	#return send_from_directory(os.path.join('..', 'src', 'static'), 'tree.jpg', as_attachment=False)
	#return send_from_directory(os.path.join('..', 'src', 'static'), 'tree.jpg', as_attachment=False)

@bp.route('/imageserver/item/<string:image_name>')
@login_required
def getItemImage(image_name):
	# TODO: Read the docs on how to improve this for server
	
	return send_from_directory(os.path.join('..', current_app.config['IMAGE_UPLOAD'], 'items'), image_name, as_attachment=False)
	