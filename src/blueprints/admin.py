from flask import (
	Blueprint, g, redirect, render_template, request, session, url_for, current_app, jsonify
)

from db import get_db, query_db

from blueprints.auth import login_required

bp = Blueprint('admin', __name__, url_prefix='/admin')

def shorten_string(string : str, max_length : int):
	shortened_name = string

	if len(string) > max_length:
		shortened_name = string[0:max_length] + '...'
	
	return shortened_name


def is_admin():
	sql_str = """SELECT Is_Admin
				FROM Users
				WHERE User_ID = ?;
			"""
	if query_db(sql_str, (session['user_id'],), True, True)['Is_Admin']	> 0:
		return True

	return False

def check_for_admin_status():
	if not is_admin():
		return redirect(url_for('auth.login'))

@bp.route('users')
@login_required
def admin_users():

	check_for_admin_status()

	sql_str = """SELECT User_ID, Username
				FROM Users
				WHERE NOT User_ID = ?;
			"""
	users = query_db(sql_str, (session['user_id'],), True)

	return render_template('admin/users.html',
							users=users)



@bp.route('users/<string:username>')
@login_required
def admin_users_characters(username):
	check_for_admin_status()

	sql_str = """SELECT User_ID
				FROM Users
				WHERE Username = ?;
			"""
	user_id = query_db(sql_str, (username,), True, True)['User_ID']

	sql_str = """SELECT Character_Name, Character_ID
				FROM Character
				WHERE User_ID = ?;
			"""
	characters = query_db(sql_str, (user_id,), True)

	return render_template('admin/characters.html',
							characters=characters)	

@bp.route('creationKit')
@login_required
def admin_creationKit():
	check_for_admin_status()

	sql_str = """SELECT Item_Name, Item_ID
				FROM Items;
			"""
	items = query_db(sql_str, (), True)

	items_mod = []

	for i in items:
		items_mod.append(
			{
				'Item_Name' : shorten_string(i['Item_Name'], 13),
				'Item_ID' : i['Item_ID']
			}
		)

	return render_template('admin/items.html',
							items=items_mod)


@bp.route('creationKit/add')
@login_required
def admin_creationKit_add():
	sql_str = """SELECT Slots_Name
				FROM SLOTS;
			"""
	slot_names = query_db(sql_str)

	sql_str = """SELECT Rarities_Name
				FROM Rarities;
			"""
	rarity_names = query_db(sql_str)

	sql_str = """SELECT Effect_Name
				FROM Effects;
			"""
	effect_names = query_db(sql_str)

	return render_template('admin/add_item.html',
							slots=slot_names,
							rarities=rarity_names,
							effects=effect_names)

@bp.route('creationKit/edit/<int:item_id>')
@login_required
def admin_creationKit_edit(item_id):
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
			'Item_Effect1_Name' : 'None',
			'Item_Effect2_Name' : 'None',
			'Item_Damage_Num_Of_Dices' : 0,
			'Item_Damage_Num_Of_Dice_Sides' : 0,
			'Item_AC_Bonus' : 0
		}

	# Check if item has an effect on it
	if itemQueryResult is not None and itemQueryResult['Item_Effect1'] is not None and itemQueryResult['Item_Effect1'] > 0:	
		# Effect1 query
		queryStr = """SELECT Effect_Name 
					FROM Effects 
					WHERE Effect_ID=?;"""
		# Check to see if ID has been assigned
		
		itemQueryResult['Item_Effect1_Name'] = query_db(queryStr, (itemQueryResult['Item_Effect1'],), True, True)['Effect_Name']

	# Check if item has an effect on it
	if itemQueryResult is not None and itemQueryResult['Item_Effect2'] is not None and itemQueryResult['Item_Effect2'] > 0:	
		# Effect2 query
		queryStr = """SELECT Effect_Name 
					FROM Effects 
					WHERE Effect_ID=?;"""
		# Check to see if ID has been assigned
		
		itemQueryResult['Item_Effect2_Name'] = query_db(queryStr, (itemQueryResult['Item_Effect2'],), True, True)['Effect_Name']

	image = url_for('static', filename='images/no_image.png')

	if itemQueryResult['Item_Picture'] is not None and itemQueryResult['Item_Picture'] != '' and itemQueryResult['Item_Picture'] != 'no_image.png':
		image = '/dataserver/imageserver/item/' + itemQueryResult['Item_Picture']


	return render_template('admin/add_item.html',
							items=itemQueryResult)

@bp.route('creationKit/remove/<int:item_id>')
@login_required
def admin_creationKit_remove(item_id):
	sql_str = """DELETE
				FROM Items
				WHERE Item_ID = ?;
			"""
	query_db(sql_str, (item_id,), False)

	return 