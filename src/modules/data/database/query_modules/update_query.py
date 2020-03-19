from modules.data.database.query import Query
from datetime import datetime

def update_item(item_data, item_id):
	update("Items", item_data, "WHERE Item_ID=?", (item_id,))

def update_isVerified(user_id, is_verified=False):
	verified_val = 0
	if is_verified:
		verified_val = 1

	update("Users", {"Is_Verified" : verified_val}, "WHERE User_ID=?", (user_id,))

def update_tos_agreement(user_id, has_agreed=False):
	agreed_val = 0
	if has_agreed:
		agreed_val = 1

	update("Users", {"Has_Agreed_TOS" : agreed_val}, "WHERE User_ID=?", (user_id,))


def update_notification_read_status(note_id, has_been_read=False):
	read = 0
	if has_been_read:
		read = 1
	update("Admin_Notifications", {"Has_Been_Read" : read}, "WHERE Note_ID=?", (note_id,))

def change_user_admin_status(user_id, is_admin=False):
	admin = 0
	if is_admin:
		admin = 1
	update("Users", {"Is_Admin" : admin}, "WHERE User_ID=?", (user_id,))

def change_num_of_login_attempts(user_id, num_of_attempts):
	update("Login_Attempts", {"Number_Attempts" : num_of_attempts}, "WHERE User_ID=?", (user_id,))

def update_attempt_datetime(user_id, datetime=datetime.utcnow()):
	update("Login_Attempts",
		{
			"Attempt_Year" : datetime.year,
			"Attempt_Month" : datetime.month,
			"Attempt_Day" : datetime.day,
			"Attempt_Hour" : datetime.hour,
			"Attempt_Minute" : datetime.minute,
			"Attempt_Second" : datetime.second
		},
		"WHERE User_ID=?",
		(user_id,)
	)

def update(table_name, data, where_clause="", where_clause_data=()):
	if len(data) < 1:
		# TODO: handle in a better way such as throwing an execption
		return

	sql_str = "UPDATE " + table_name + " SET "

	num_of_fields = len(data)
	count = 0
	args=[]

	for key in data:
		args.append(data[key])
		sql_str += key + "=?"
		if count < num_of_fields - 1:
			sql_str += ", "
		count += 1

	sql_str += where_clause + ";"

	for d in where_clause_data:
		args.append(d)

	## TODO: see the delete query todo
	return Query(sql_str, tuple(args), False).run_query()