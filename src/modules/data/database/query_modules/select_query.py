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

    sql_str += " FROM " + from_table + " "
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

def select_char_id_from_name(user_id, char_name):
    where_clause = "WHERE User_ID=? AND Character_Name=?"
    return select(("Character_ID",), "Character", False, where_clause, (user_id, char_name))

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

def get_class_names(class_id):
    sql_str = """SELECT Class_Name
                FROM Class
                WHERE Class_ID = ?;
            """
    result = Query(sql_str, (class_id,)).run_query()
    if result is not None:
        return result['Class_Name']

    return result

def select_character_class(user_id, char_id):
    return select(("Class_Name",), "Character", False, "WHERE User_ID=? AND Character_ID=?",
                    (user_id, char_id), ("INNER JOIN Class ON Class.Class_ID = Character.Character_Class",))

def select_character_race(user_id, char_id):
    return select(("Race_Name",), "Character", False, "WHERE User_ID=? AND Character_ID=?",
                    (user_id, char_id), ("INNER JOIN Races ON Races.Race_ID = Character.Character_Race",))

def get_race_name_from_id(race_id):
    where_clause = "WHERE Race_ID=?"
    result = select(("Race_Name",), "Races", False, where_clause, (race_id,))

    if result is not None:
        return result['Race_Name']

    return result

def get_race_id_from_name(race_name):
    where_clause = "WHERE Race_Name=?"
    result = select(("Race_ID",), "Races", False, where_clause, (race_name,))

    if result is not None:
        return result['Race_ID']

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

def get_alignments():
    return select(("Alignment_ID", "Alignment_Name"), "Alignments", True)

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
        # TODO: this should throw an exception, but for now it will just be logged
        Logger.error("Invalid query attempted to run")
    elif query_result['Is_Admin'] > 0:
        return True

    return False

def select_effect_data(effect_id):
    return select(("*",), "Effects", False, "WHERE Effect_ID=?", (effect_id,))

def select_char_fields(user_id, char_id, field_names=("*",), joins=()):
    return select(field_names, "Character", False, "WHERE User_ID=? AND Character_ID=?", (user_id, char_id), joins)

def select_item_fields(item_id, field_names=("*",), joins=()):
    return select(field_names, "Items", False, "WHERE Item_ID=?", (item_id,), joins)

def select_item_fields_from_item_slot(item_slot_num, field_names=("*",)):
    return select(field_names, "Items", True, "WHERE Item_Slot=?", (item_slot_num,), ("INNER JOIN Rarities on Rarities.Rarities_ID=Items.Rarity_ID",))

def select_item_data_from_inventory(char_id):
    fields = ("Items.Item_ID", "Items.Item_Weight", "Items.Item_Name", "Items.Item_Slot",
                "Rarities.Rarities_Color", "Slots.Slots_Name", "Inventory.Amount", "Item_Picture")
    joins = (
        "INNER JOIN Items on Inventory.Item_ID=Items.Item_ID",
        "INNER JOIN Rarities on Rarities.Rarities_ID=Items.Rarity_ID",
        "INNER JOIN Slots on Items.Item_Slot=Slots.Slots_ID"
    )
    where_clause = "WHERE Inventory.Character_ID = ?"
    return select(fields, "Inventory", True, where_clause, (char_id,), joins)

def get_class_id_from_name(class_name):
    where_clause = "WHERE Class_Name=?"
    result = select(("Class_ID",), "Class", False, where_clause, (class_name,))

    if result is not None:
        return result['Class_ID']

    return result

def get_alignment_id_from_name(alignment_name):
    where_clause = "WHERE Alignment_Name=?"
    result = select(("Alignment_ID",), "Alignments", False, where_clause, (alignment_name,))

    if result is not None:
        return result['Alignment_ID']

    return result

def select_item_amount_from_inv(char_id, item_id):
    fields = ("Amount",)
    where_clause = "WHERE Character_ID=? AND Inventory.Item_ID=?"
    return select(fields, "Inventory", False, where_clause, (char_id, item_id))

def select_item_picture_name(item_id):
    return select(("Item_Picture",), "Items", False, "WHERE Item_ID=?", (item_id,))

def select_site_notifications():
    return select(("*",), "Site_Notifications", True)

def select_character_skills(char_id):
    joins = (
        "INNER JOIN Skills on Character_Skills.Skill_ID=Skills.Skill_ID",
    )
    fields = (
        "Character_Skills.Skill_ID",
        "Character_Skills.Skill_Base_Value",
        "Skills.Skill_Name",
        "Skills.Skill_Type"
    )
    return select(fields, "Character_Skills", True, "WHERE Character_ID=?", (char_id,), joins)

def select_all_skills():
    return select(("*",), "Skills", True)

def select_skill_id_from_name(skill_name):
    return select(("Skill_ID",), "Skills", False, "WHERE Skill_Name=?", (skill_name,))

def select_char_skill(char_id, skill_id=-1):
    where_clause = "WHERE Character_ID=?"
    args = [char_id]
    multiple = True
    if skill_id > -1:
        where_clause += " AND Skill_ID=?"
        args.append(skill_id)
        multiple = False

    return select(("*",), "Character_Skills", multiple, where_clause, tuple(args))

def select_abilities(char_id, ability_id=-1):
    where_clause = "WHERE Character_ID=?"
    args = [char_id]
    multiple = True
    if ability_id > -1:
        where_clause += " AND Ability_ID=?"
        args.append(ability_id)
        multiple = False

    return select(("*",), "Abilities", multiple, where_clause, tuple(args))

def select_ability_id_from_name(ability_name):
    return select(("Ability_ID",), "Abilities", False, "WHERE Ability_Name=?", (ability_name,))
