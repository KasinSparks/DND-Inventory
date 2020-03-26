from modules.data.database.query import Query

def insert(table_name, item_data):
	if len(item_data) < 1:
		# TODO: handle in a better way such as throwing an execption
		return

	sql_str = "INSERT INTO " + table_name + " ("
	values_str = "VALUES ("

	num_of_fields = len(item_data)
	count = 0

	args = []

	for key in item_data:
		sql_str += key
		values_str += "?"
		args.append(item_data[key])
		if count < num_of_fields - 1:
			sql_str += ", "
			values_str += ","
		else:
			sql_str += ") "
			values_str += ")"
		count += 1

	sql_str +=  values_str + ";"

	## TODO: see the delete query todo
	Query(sql_str, tuple(args), False).run_query()

def insert_effect(name, description):
	insert("Effects", {"Effect_Name" : name, "Effect_Description" : description})

def create_user(username, hashed_password):
	insert("Users", {"Username" : username, "Password" : hashed_password})

def create_admin_notification(user_id, notification_type):
	insert("Admin_Notifications", 
		{
			"User_ID" : user_id,
			"Notification_Type" : notification_type,
			"Has_Been_Read" : 0
		}
	)

def create_login_attempt(user_id):
	insert("Login_Attempts", {"User_ID" : user_id})

def create_race(race_name):
	insert("Races", {"Race_Name" : race_name})
	
def create_class(class_name):
	insert("Class", {"Class_Name" : class_name})
	
def create_alignment(alignment_name):
	insert("Alignments", {"Alignment_Name" : alignment_name})

def create_character(data):
	insert("Character", data)