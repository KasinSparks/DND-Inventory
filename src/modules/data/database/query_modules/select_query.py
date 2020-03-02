from modules.data.database.query import Query

def select_user_data_except_user(user_id):
	sql_str = """SELECT User_ID, Username, Is_Verified, Is_Admin
			FROM Users
			WHERE NOT User_ID = ?;
		"""
	return Query(sql_str, (user_id,), True, True).run_query()

def get_user_id(username):
	sql_str = """SELECT User_ID
				FROM Users
				WHERE Username = ?;
			"""
	return Query(sql_str, (username,), True, True).run_query()['User_ID']

def	select_char_name_and_id(user_id):
	sql_str = """SELECT Character_Name, Character_ID
				FROM Character
				WHERE User_ID = ?;
			"""
	return Query(sql_str, (user_id,)).run_query()

def select_items_name_and_id():
	sql_str = """SELECT Item_Name, Item_ID
				FROM Items;
			"""
	return Query(sql_str).run_query()

def select_slot_names(slot_id = -1):
	where_command = ""
	args = ()
	multi = False

	if slot_id > -1:
		where_command = "WHERE Slot_ID=?"
		args = (slot_id,)
		multi = True

	sql_str = """SELECT Slots_Name
				FROM Slots""" + where_command + ";"
	return Query(sql_str, args, True, multi).run_query()

def select_rarity_names():
	sql_str = """SELECT Rarities_Name
				FROM Rarities;
			"""
	return Query(sql_str).run_query()

def select_effect_names(effect_id = -1):
	where_command = ""
	args = ()
	multi = False

	if effect_id > -1:
		where_command = "WHERE Effect_ID=?"
		args = (effect_id,)
		multi = True


	sql_str = """SELECT Effect_Name
				FROM Effects""" + where_command + ";"

	return Query(sql_str, args, True, multi).run_query()

def select_items(item_id = -1):
	where_command = ""
	args = ()
	multi = False

	if item_id > -1:
		where_command = "WHERE Items.Item_ID=?"
		args = (item_id,)
		multi = True

	sql_str = """SELECT *
				FROM Items
				LEFT JOIN Rarities ON Items.Rarity_ID=Rarities.Rarities_ID
				INNER JOIN Slots ON Items.Slot=Slots.Slots_ID""" + where_command + ";"

	return Query(sql_str, args, True, multi)	

