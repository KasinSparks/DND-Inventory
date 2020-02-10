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

	if itemQueryResult['Item_Picture'] is not None and itemQueryResult['Item_Picture'] != '' and itemQueryResult['Item_Picture'] != 'no_image.png':
		item_encoded = convert_image_to_base64(os.path.join(current_app.config['IMAGE_UPLOAD'], itemQueryResult['Item_Picture']))
	else:
		item_encoded = convert_image_to_base64(os.path.join('src', 'static', 'images', itemQueryResult['Item_Picture']))

	return jsonify(description=itemQueryResult['Item_Description'],
					name=itemQueryResult['Item_Name'],
					encoded_image=item_encoded['encoded_image'],
					image_type=item_encoded['image_type'],
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