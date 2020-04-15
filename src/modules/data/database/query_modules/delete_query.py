from modules.data.database.query import Query

def delete_item(item_id):
    delete("Items", "WHERE Item_ID=?", (item_id,))
    delete("Inventory", "WHERE Item_ID=?", (item_id,))

def delete_notification(notification_id):
    delete("Admin_Notifications", "WHERE Note_ID=?", (notification_id,))

def delete_users_notifications(user_id):
    delete("Admin_Notifications", "WHERE User_ID=?", (user_id,))

def delete_user(user_id):
    delete("Users", "WHERE User_ID=?", (user_id,))

def delete_character_abilites(char_id):
    delete("Abilites", "WHERE Character_ID=?", (char_id,))

def delete_character_skill(char_id):
    delete("Character_Skills", "WHERE Character_ID=?", (char_id,))

def delete_character_inventory(char_id):
    delete("Inventory", "WHERE Character_ID=?", (char_id,))

def delete_users_characters(user_id):
    delete("Character", "WHERE User_ID=?", (user_id,))

def delete_login_attempts(user_id):
    delete("Login_Attempts", "WHERE User_ID=?", (user_id,))

def delete_item_from_inv(char_id, item_id):
    delete("Inventory", "WHERE Item_ID=? AND Character_ID=?", (item_id, char_id))

#def delete_ability(char_id, ability_id):
#    delete("Abilities", "WHERE Ability_ID=? AND Character_ID=?", (ability_id, char_id))

def delete(table_name, where_clause="", where_clause_data=()):
    sql_str = """DELETE FROM """ + table_name + " "
    sql_str += where_clause + ";"

    ## TODO: not sure if this will return anything useful... need to look into it
    Query(sql_str, where_clause_data, False).run_query()

