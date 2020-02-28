from flask import (
	Blueprint, g, redirect, render_template, request, session, url_for, current_app, jsonify
)

import os

from werkzeug import secure_filename

from db import get_db, query_db

from blueprints.auth import login_required, get_current_username

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

	sql_str = """SELECT User_ID, Username, Is_Verified
				FROM Users
				WHERE NOT User_ID = ?;
			"""
	users = query_db(sql_str, (session['user_id'],), True)

	user_data = []

	for u in users:
		user_data.append(
			{
				'User_ID' : u['User_ID'],
				'Username' : shorten_string(u['Username'], 16),
				'Is_Verified' : u['Is_Verified']
			}
		)

	return render_template('admin/users.html',
							users=user_data,
							header_text=get_current_username())



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
							characters=characters,
							header_text=get_current_username())	

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
							items=items_mod,
							header_text=get_current_username())


@bp.route('creationKit/add')
@login_required
def admin_creationKit_add():
	check_for_admin_status()
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
							effects=effect_names,
							header_text=get_current_username())

@bp.route('creationKit/edit/<int:item_id>')
@login_required
def admin_creationKit_edit(item_id):
	check_for_admin_status()

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
			'Item_Attack_Bonus' : 0,
			'Item_Initiative_Bonus' : 0,
			'Item_Health_Bonus' : 0,
			'Item_Damage_Num_Of_Dices' : 0,
			'Item_Damage_Num_Of_Dice_Sides' : 0,
			'Item_AC_Bonus' : 0
		}

	item_effect1 = 'None'
	item_effect2 = 'None'
	item_slots_name = ''

	# Check if item has an effect on it
	if itemQueryResult is not None and itemQueryResult['Item_Effect1'] is not None and itemQueryResult['Item_Effect1'] > 0:	
		# Effect1 query
		queryStr = """SELECT Effect_Name 
					FROM Effects 
					WHERE Effect_ID=?;"""
		# Check to see if ID has been assigned
		
		item_effect1 = query_db(queryStr, (itemQueryResult['Item_Effect1'],), True, True)['Effect_Name']

	# Check if item has an effect on it
	if itemQueryResult is not None and itemQueryResult['Item_Effect2'] is not None and itemQueryResult['Item_Effect2'] > 0:	
		# Effect2 query
		queryStr = """SELECT Effect_Name 
					FROM Effects 
					WHERE Effect_ID=?;"""
		# Check to see if ID has been assigned
		
		item_effect2 = query_db(queryStr, (itemQueryResult['Item_Effect2'],), True, True)['Effect_Name']

	
	if itemQueryResult is not None and itemQueryResult['Item_Slot'] is not None and itemQueryResult['Item_Slot'] > 0:	
		# Effect2 query
		queryStr = """SELECT Slots_Name 
					FROM Slots 
					WHERE Slots_ID=?;"""
		# Check to see if ID has been assigned
		
		item_slots_name = query_db(queryStr, (itemQueryResult['Item_Slot'],), True, True)['Slots_Name']

	image = url_for('static', filename='images/no_image.png')

	if itemQueryResult['Item_Picture'] is not None and itemQueryResult['Item_Picture'] != '' and itemQueryResult['Item_Picture'] != 'no_image.png':
		image = '/dataserver/imageserver/item/' + itemQueryResult['Item_Picture']


	return render_template('admin/edit_item.html',
							items=itemQueryResult,
							slots=slot_names,
							rarities=rarity_names,
							effects=effect_names,
							effect1_name=item_effect1,
							effect2_name=item_effect2,
							item_id=item_id,
							item_slots_name=item_slots_name,
							header_text=get_current_username())

@bp.route('creationKit/remove/<int:item_id>')
@login_required
def admin_creationKit_remove(item_id):
	check_for_admin_status()
	sql_str = """DELETE
				FROM Items
				WHERE Item_ID = ?;
			"""
	query_db(sql_str, (item_id,), False)

	return redirect(url_for('admin.admin_creationKit'))

@bp.route('creationKit/add/submit', methods=('GET', 'POST'))
@login_required
def admin_creationKit_add_submit():
	check_for_admin_status()
	if request.method == 'POST':
		insert_sql_str = """INSERT INTO Items (Item_Name, Item_Picture, Item_Description,
								Item_Slot, Rarity_ID, Item_Weight, Item_Str_Bonus, Item_Dex_Bonus
								, Item_Con_Bonus, Item_Int_Bonus, Item_Wis_Bonus, Item_Cha_Bonus, Item_Effect1,
								Item_Effect2, Item_Attack_Bonus, Item_Initiative_Bonus,
								Item_Health_Bonus, Item_AC_Bonus, Item_Damage_Num_Of_Dices,
								Item_Damage_Num_Of_Dice_Sides)
							VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
				"""

		sql_str = """SELECT Item_ID
					FROM Items
					WHERE Item_Name = ?;
				"""
		name_check = query_db(sql_str, (get_request_field_data('name'), ), True, True)
		
		if name_check is not None:
			# Name already exist
			return '[TODO: Change this later]\n\nItem name already exist... Please go back and try again.'

		sql_str = """SELECT Slots_ID
					FROM Slots
					WHERE Slots_Name = ?;
				"""
		slot_id = query_db(sql_str, (request.form['slot'],), True, True)
		if slot_id is None:
			raise Exception('Not a valid slot')
		else:
			slot_id = int(slot_id['Slots_ID'])

		sql_str = """SELECT Rarities_ID
					FROM Rarities 
					WHERE Rarities_Name = ?;
				"""
		rarity_id = query_db(sql_str, (request.form['rarity'],), True, True)
		if rarity_id is None:
			raise Exception('Not a valid rarity')
		else:
			rarity_id = int(rarity_id['Rarities_ID'])

		effect1_val = request.form['effect1']
		effect2_val = request.form['effect2']

		if effect1_val == 'OTHER':
			create_new_effect(request.form['effect1_name'], request.form['effect1_description'])	
			effect1_val = request.form['effect1_name']

		if effect2_val == 'OTHER':
			create_new_effect(request.form['effect2_name'], request.form['effect2_description'])	
			effect2_val = request.form['effect2_name']

		sql_str = """SELECT Effect_ID
					FROM Effects
					WHERE Effect_Name = ?;
				"""
		effect1_id = query_db(sql_str, (effect1_val,), True, True)
		if effect1_id is None:
			raise Exception('Not a valid effect1')
		else:
			effect1_id = int(effect1_id['Effect_ID'])

		effect2_id = query_db(sql_str, (effect2_val,), True, True)
		if effect2_id is None:
			raise Exception('Not a valid effect2')
		else:
			effect2_id = int(effect2_id['Effect_ID'])

		filename = 'no_image.png'
		
		if 'picture' not in request.files:
			new_img = request.files['picture']

			if new_img.filename == '':
				return 'File name was blank'

			if new_img and allowed_file(new_img.filename):
				filename = secure_filename(new_img.filename)
				dirName = 'items'
				fullDirName = os.path.join(current_app.config['IMAGE_UPLOAD'], dirName)

				if not os.path.exists(fullDirName):
					os.mkdir(fullDirName, mode=0o770)

				new_img.save(os.path.join(fullDirName, filename))


		query_db(insert_sql_str, 
			(
				str(get_request_field_data('name')),
				filename,	
				str(get_request_field_data('description')),
				slot_id,
				rarity_id,
				convert_form_field_data_to_int(get_request_field_data('weight')),
				convert_form_field_data_to_int(get_request_field_data('str_bonus')),
				convert_form_field_data_to_int(get_request_field_data('dex_bonus')),
				convert_form_field_data_to_int(get_request_field_data('con_bonus')),
				convert_form_field_data_to_int(get_request_field_data('int_bonus')),
				convert_form_field_data_to_int(get_request_field_data('wis_bonus')),
				convert_form_field_data_to_int(get_request_field_data('cha_bonus')),
				effect1_id,
				effect2_id,
				convert_form_field_data_to_int(get_request_field_data('attack_bonus')),
				convert_form_field_data_to_int(get_request_field_data('initiative_bonus')),
				convert_form_field_data_to_int(get_request_field_data('health_bonus')),
				convert_form_field_data_to_int(get_request_field_data('ac_bonus')),
				convert_form_field_data_to_int(get_request_field_data('dnof')),
				convert_form_field_data_to_int(get_request_field_data('dnofs')),

			),
			False
		)

		return redirect(url_for('admin.admin_creationKit'))

@bp.route('creationKit/edit/submit', methods=('GET', 'POST'))
@login_required
def admin_creationKit_edit_submit():
	check_for_admin_status()
	if request.method == 'POST':
		insert_sql_str = """UPDATE Items
							SET Item_Name=?, Item_Picture=?, Item_Description=?,
								Item_Slot=?, Rarity_ID=?, Item_Weight=?, Item_Str_Bonus=?, Item_Dex_Bonus=?
								, Item_Con_Bonus=?, Item_Int_Bonus=?, Item_Wis_Bonus=?, Item_Cha_Bonus=?, Item_Effect1=?,
								Item_Effect2=?, Item_Attack_Bonus=?, Item_Initiative_Bonus=?,
								Item_Health_Bonus=?, Item_AC_Bonus=?, Item_Damage_Num_Of_Dices=?,
								Item_Damage_Num_Of_Dice_Sides=?
							WHERE Item_ID = ?;
				"""


		sql_str = """SELECT Slots_ID
					FROM Slots
					WHERE Slots_Name = ?;
				"""
		slot_id = query_db(sql_str, (request.form['slot'],), True, True)
		if slot_id is None:
			raise Exception('Not a valid slot')
		else:
			slot_id = int(slot_id['Slots_ID'])

		sql_str = """SELECT Rarities_ID
					FROM Rarities 
					WHERE Rarities_Name = ?;
				"""
		rarity_id = query_db(sql_str, (request.form['rarity'],), True, True)
		if rarity_id is None:
			raise Exception('Not a valid rarity')
		else:
			rarity_id = int(rarity_id['Rarities_ID'])

		effect1_val = request.form['effect1']
		effect2_val = request.form['effect2']

		if effect1_val == 'OTHER':
			create_new_effect(request.form['effect1_name'], request.form['effect1_description'])	
			effect1_val = request.form['effect1_name']

		if effect2_val == 'OTHER':
			create_new_effect(request.form['effect2_name'], request.form['effect2_description'])	
			effect2_val = request.form['effect2_name']

		sql_str = """SELECT Effect_ID
					FROM Effects
					WHERE Effect_Name = ?;
				"""
		effect1_id = query_db(sql_str, (effect1_val,), True, True)
		if effect1_id is None:
			#raise Exception('Not a valid effect1')
			effect1_id = -1 
		else:
			effect1_id = int(effect1_id['Effect_ID'])

		effect2_id = query_db(sql_str, (effect2_val,), True, True)
		if effect2_id is None:
			effect2_id = -1 
			#raise Exception('Not a valid effect2')
		else:
			effect2_id = int(effect2_id['Effect_ID'])


		filename = 'no_image.png'

		if 'picture' not in request.files:
			new_img = request.files['picture']

			if new_img.filename == '':
				return 'File name was blank'

			if new_img and allowed_file(new_img.filename):
				sql_str = """SELECT Item_Picture
							FROM Items
							WHERE Item_ID = ?;
						"""
				existing_picture_name = query_db(sql_str, (int(get_request_field_data('id')),), True, True)['Item_Picture']
				filename = secure_filename(new_img.filename)
				if existing_picture_name != filename:
					dirName = 'items'
					fullDirName = os.path.join(current_app.config['IMAGE_UPLOAD'], dirName)

					if not os.path.exists(fullDirName):
						os.mkdir(fullDirName, mode=0o770)

					new_img.save(os.path.join(fullDirName, filename))


		query_db(insert_sql_str, 
			(
				str(get_request_field_data('name')),
				filename,	
				str(get_request_field_data('description')),
				slot_id,
				rarity_id,
				convert_form_field_data_to_int(get_request_field_data('weight')),
				convert_form_field_data_to_int(get_request_field_data('str_bonus')),
				convert_form_field_data_to_int(get_request_field_data('dex_bonus')),
				convert_form_field_data_to_int(get_request_field_data('con_bonus')),
				convert_form_field_data_to_int(get_request_field_data('int_bonus')),
				convert_form_field_data_to_int(get_request_field_data('wis_bonus')),
				convert_form_field_data_to_int(get_request_field_data('cha_bonus')),
				effect1_id,
				effect2_id,
				convert_form_field_data_to_int(get_request_field_data('attack_bonus')),
				convert_form_field_data_to_int(get_request_field_data('initiative_bonus')),
				convert_form_field_data_to_int(get_request_field_data('health_bonus')),
				convert_form_field_data_to_int(get_request_field_data('ac_bonus')),
				convert_form_field_data_to_int(get_request_field_data('dnof')),
				convert_form_field_data_to_int(get_request_field_data('dnofs')),
				int(get_request_field_data('id'))
			),
			False
		)

		return redirect(url_for('admin.admin_creationKit'))

@bp.route('users/verify/<int:user_id>')
@login_required
def admin_verify_user(user_id):
	check_for_admin_status()
	sql_str = """UPDATE Users
				SET Is_Verified = 1
				WHERE User_ID = ?;
			"""
	query_db(sql_str, (user_id, ), False)
	return '200'


@bp.route('notifications')
@login_required
def admin_notifications():
	check_for_admin_status()
	sql_str = """SELECT Note_ID, Admin_Notifications.User_ID, Type, Username, Has_Been_Read, Notification_ID
				FROM Admin_Notifications
				INNER JOIN Notification_Types ON Admin_Notifications.Notification_Type=Notification_Types.Notification_ID
				INNER JOIN Users ON Admin_Notifications.User_ID=Users.User_ID
				;
			"""	
	notifications = query_db(sql_str)

	return render_template('admin/notifications.html',
							header_text=get_current_username(),
							notifications=notifications)


@bp.route('notifications/remove/<int:notification_id>')
@login_required
def admin_remove_notification(notification_id):
	sql_str = """DELETE FROM Admin_Notifications
				WHERE Note_ID=?;
			"""
	query_db(sql_str, (notification_id,), False)
	return '200'

@bp.route('notifications/markRead/<int:notification_id>')
@login_required
def admin_markRead_notification(notification_id):
	sql_str = """UPDATE Admin_Notifications
				SET Has_Been_Read = 1
				WHERE Note_ID=?;
			"""
	query_db(sql_str, (notification_id,), False)
	return '200'

@bp.route('users/remove', methods=('GET', 'POST'))
@login_required
def admin_remove_user():
	if request.method != 'POST':
		return '400'

	user_id = request.form['user_id']

	sql_str = """DELETE FROM Users 
				WHERE User_ID=?;
			"""
	query_db(sql_str, (user_id,), False)

	sql_str = """SELECT Character_ID
				FROM Character
				WHERE User_ID = ?;
			"""
	characters = query_db(sql_str, (user_id,), True)

	for c in characters:
		char_id = c['Character_ID']

		sql_str = """DELETE FROM Character_Abilites
					WHERE Character_ID=?;
				"""
		query_db(sql_str, (char_id,), False)

		sql_str = """DELETE FROM Character_Skills
					WHERE Character_ID=?;
				"""
		query_db(sql_str, (char_id,), False)

		sql_str = """DELETE FROM Inventory 
					WHERE Character_ID=?;
				"""
		query_db(sql_str, (char_id,), False)


	sql_str = """DELETE FROM Character 
				WHERE User_ID=?;
			"""
	query_db(sql_str, (user_id,), False)

	sql_str = """DELETE FROM Login_Attempts 
				WHERE User_ID=?;
			"""
	query_db(sql_str, (user_id,), False)

	sql_str = """DELETE FROM Admin_Notifications 
				WHERE User_ID=?;
			"""
	query_db(sql_str, (user_id,), False)

	return '200'



def allowed_file(filename):
	 return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def create_new_effect(effect_name, effect_description):
	if effect_name is None or effect_name == '' or effect_description is None or effect_description == '':
		raise Exception('Invalid effect')

	sql_str = """INSERT INTO Effects (Effect_Name, Effect_Description)
				VALUES (?, ?);
			"""
	query_db(sql_str, (effect_name, effect_description), False)

def get_request_field_data(field_name):
	print(str(field_name) + ' : ' + str(request.form[field_name]))
	return request.form[field_name]

def convert_form_field_data_to_int(field_data):
	return 0 if field_data is None or field_data == '' else int(field_data)