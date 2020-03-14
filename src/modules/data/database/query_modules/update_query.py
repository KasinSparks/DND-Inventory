from modules.data.database.query import Query

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