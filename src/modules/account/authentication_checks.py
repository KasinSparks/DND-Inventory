from flask import session, redirect, url_for
from modules.data.database.query_modules.select_query import get_is_admin

def check_for_admin_status():
	if not get_is_admin(session['user_id']):
		return redirect(url_for('auth.login'))