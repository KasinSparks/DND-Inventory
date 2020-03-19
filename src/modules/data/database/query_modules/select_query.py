from modules.data.database.query import Query
from logger.logger import Logger

# TODO: make more moduler like update and others
# TODO: error/null checking on the queries that are being index

def select(select_fields, from_table, multiple=False, where_clause="", args=(), joins=()):
	sql_str = "SELECT "
	num_of_fields = len(select_fields)
	count = 0
	for field in select_fields:
		sql_str += field
		if count < num_of_fields - 1:
			sql_str += ", "	
		count += 1

	sql_str += "FROM " + from_table + " "
	for join in joins:
		sql_str += join + " "

	sql_str += where_clause + ";"
	return Query(sql_str, args, True, multiple).run_query()

def select_user_data_except_user(user_id):
	sql_str = """SELECT User_ID, Username, Is_Verified, Is_Admin
			FROM Users
			WHERE NOT User_ID = ?;
		"""
	return Query(sql_str, (user_id,), True, True).run_query()

def select_user_data(username):
	sql_str = """SELECT *
				FROM Users
				WHERE Username = ?;
			"""
	return Query(sql_str, (username,), True, False).run_query()

def select_user_data_from_id(user_id):
	sql_str = """SELECT *
				FROM Users
				WHERE User_ID=?;
			"""
	return Query(sql_str, (user_id,)).run_query()

def get_username(user_id):
	sql_str = """SELECT Username 
				FROM Users
				WHERE User_ID=?;
			"""
	result = Query(sql_str, (user_id,)).run_query()
	if result is not None:
		return result['Username']

	return result


def get_user_id(username):
	sql_str = """SELECT User_ID
				FROM Users
				WHERE Username = ?;
			"""
	result = Query(sql_str, (username,), True, False).run_query()
	if result is not None:
		return result['User_ID']

	return result

def	select_char_name_and_id(user_id):
	sql_str = """SELECT Character_Name, Character_ID
				FROM Character
				WHERE User_ID = ?;
			"""
	return Query(sql_str, (user_id,), True, True).run_query()

def get_char_id(user_id):
	sql_str = """SELECT Character_ID
				FROM Character 
				WHERE User_ID= ?;
			"""
	return Query(sql_str, (user_id,), True, True).run_query()

def select_character_data(char_id, user_id=-1):
	sql_str = """SELECT *
				FROM Character
				WHERE Character_ID=?
			"""
	args = [char_id]
	if user_id > 0:
		sql_str += " AND User_ID=?"
		args.append(user_id)
	sql_str += ";"
	return Query(sql_str, tuple(args)).run_query()

def select_items_name_and_id():
	sql_str = """SELECT Item_Name, Item_ID
				FROM Items;
			"""
	return Query(sql_str, multiple=True).run_query()

def select_slot_names(slot_id = -1):
	where_command = ""
	args = ()
	multi = True

	if slot_id > -1:
		where_command = "WHERE Slots_ID=?"
		args = (slot_id,)
		multi = False 

	sql_str = """SELECT Slots_Name
				FROM Slots """ + where_command + ";"
	return Query(sql_str, args, True, multi).run_query()

def select_rarity_names():
	sql_str = """SELECT Rarities_Name
				FROM Rarities;
			"""
	return Query(sql_str, multiple=True).run_query()

def select_effect_names(effect_id = -1):
	where_command = ""
	args = ()
	multi = True 

	if effect_id > -1:
		where_command = "WHERE Effect_ID=?"
		args = (effect_id,)
		multi = False


	sql_str = """SELECT Effect_Name
				FROM Effects """ + where_command + ";"

	return Query(sql_str, args, True, multi).run_query()

def select_items(item_id = -1):
	where_command = ""
	args = ()
	multi = True 

	if item_id > -1:
		where_command = "WHERE Items.Item_ID=?"
		args = (item_id,)
		multi = False 

	sql_str = """SELECT *
				FROM Items
				LEFT JOIN Rarities ON Items.Rarity_ID=Rarities.Rarities_ID
				INNER JOIN Slots ON Items.Item_Slot=Slots.Slots_ID """ + where_command + ";"

	return Query(sql_str, args, True, multi).run_query()

def get_item_id_from_name(item_name):
	sql_str = """SELECT Item_ID
				FROM Items
				WHERE Item_Name = ?;
			"""
	result = Query(sql_str, (item_name,)).run_query()
	if result is not None:
		return result['Item_ID']

	return result

def get_slot_id_from_name(slot_name):
	sql_str = """SELECT Slots_ID
				FROM Slots
				WHERE Slots_Name = ?;
			"""
	result = Query(sql_str, (slot_name,)).run_query()
	if result is not None:
		return result['Slots_ID']

	return result

def get_rarity_id_from_name(rarity_name):
	sql_str = """SELECT Rarities_ID
				FROM Rarities
				WHERE Rarities_Name = ?;
			"""
	result = Query(sql_str, (rarity_name,)).run_query()
	if result is not None:
		return result['Rarities_ID']

	return result

def select_effect_id_from_name(effect_name):
	sql_str = """SELECT Effect_ID
				FROM Effects
				WHERE Effect_Name = ?;
			"""
	return Query(sql_str, (effect_name,)).run_query()

def select_notifications():
	sql_str = """SELECT Note_ID, Admin_Notifications.User_ID, Type, Username, Has_Been_Read, Notification_ID
				FROM Admin_Notifications
				INNER JOIN Notification_Types ON Admin_Notifications.Notification_Type=Notification_Types.Notification_ID
				INNER JOIN Users ON Admin_Notifications.User_ID=Users.User_ID;
			"""	
	return Query(sql_str, (), True, True).run_query()

def get_has_agreed_to_tos(user_id):
	sql_str = """SELECT Has_Agreed_TOS
				FROM Users
				WHERE User_ID=?;
			"""
	return Query(sql_str, (user_id,)).run_query()['Has_Agreed_TOS']

def get_notification_id(notification_type):
	sql_str = """SELECT Notification_ID 
				FROM Notification_Types
				WHERE Type = ?;
				"""
	result = Query(sql_str, (notification_type,)).run_query()
	if result is not None:
		return result['Notification_ID']

	return result

def get_class_name(class_id):
	sql_str = """SELECT Class_Name
				FROM Class
				WHERE Class_ID = ?;
			"""
	result = Query(sql_str, (class_id,)).run_query()
	if result is not None:
		return result['Class_Name']

	return result

def get_race_name(race_id):
	sql_str = """SELECT Race_Name
				FROM Races
				WHERE Race_ID = ?;
			"""
	result = Query(sql_str, (race_id,)).run_query()
	if result is not None:
		return result['Race_Name']

	return result

def get_alignment_name(alignment_id):
	sql_str = """SELECT Alignment_Name
				FROM Alignments
				WHERE Alignment_ID = ?;
			"""
	result = Query(sql_str, (alignment_id,)).run_query()
	if result is not None:
		return result['Alignment_Name']

	return result

def select_slots():
	sql_str = """SELECT *
				FROM SLOTS;
		"""
	return Query(sql_str, multiple=True).run_query()

def select_attempt_date(user_id):
	return select(
		("Attempt_Year", "Attempt_Month", "Attempt_Day", "Attempt_Hour", "Attempt_Minute", "Attempt_Second"),
		"Login_Attempts",
		False,
		"WHERE User_ID=?",
		(user_id,)
	)

def get_num_of_login_attempts(user_id):
	return select(("Number_Attempts",), "Login_Attempts", False, "WHERE User_ID=?", (user_id,))

def get_is_admin(user_id):
	query_result = select(("Is_Admin",), "Users", False, "WHERE User_ID=?", (user_id,))
	if query_result is None:
		#raise Exception("Invalid query attempted to run.")
		# TODO: this should prop. throw an exception, but for now it will just be logged
		Logger.error("Invalid query attempted to run")
	elif query_result['Is_Admin'] > 0:
		return True

	return False 