from modules.data.database.query import Query

def delete_item(item_id):
	return delete("Items", "WHERE Item_ID=?", (item_id,))

def delete_notification(notification_id):
	return delete("Admin_Notifications", "WHERE Note_ID=?", (notification_id,))

def delete_users_notifications(user_id):
	return delete("Admin_Notifications", "WHERE User_ID=?", (user_id,))

def delete_user(user_id):
	return delete("Users", "WHERE User_ID=?", (user_id,))

def delete_character_abilites(char_id):
	return delete("Character_Abilites", "WHERE Character_ID=?", (char_id,))

def delete_character_skill(char_id):
	return delete("Character_Skills", "WHERE Character_ID=?", (char_id,))

def delete_character_inventory(char_id):
	return delete("Inventory", "WHERE Character_ID=?", (char_id,))

def delete_users_characters(user_id):
	return delete("Character", "WHERE User_ID=?", (user_id,))

def delete_login_attempts(user_id):
	return delete("Login_Attempts", "WHERE User_ID=?", (user_id,))

	
def delete(table_name, where_clause="", where_clause_data=()):
	sql_str = """DELETE FROM """ + table_name + " "
	sql_str += where_clause + ";"

	## TODO: not sure if this will return anything useful... need to look into it
	return Query(sql_str, where_clause_data, False).run_query()

