from flask import session, redirect, url_for
from modules.data.database.db import query_db

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