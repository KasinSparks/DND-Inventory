from flask import session, redirect, url_for
from modules.data.database.query_modules import select_query 

def check_for_admin_status():
    if not select_query.get_is_admin(session['user_id']):
        return redirect(url_for('auth.login'))

def is_admin():
    return select_query.get_is_admin(session['user_id'])

def check_if_user_has_character(user_id, char_id):
    has_char = select_query.select_char_fields(user_id, char_id, ("Character_ID",)) 

    if has_char is not None:
        return True 
    
    return False