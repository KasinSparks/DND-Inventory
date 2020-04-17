from flask import session, redirect, url_for, render_template
from modules.data.database.query_modules import select_query

# Depercated
#def check_for_admin_status():
#    if not select_query.get_is_admin(session['user_id']):
#        return redirect(url_for('auth.login'))

def not_admin_redirect():
    return redirect(url_for('auth.login'))

def is_admin():
    return select_query.get_is_admin(session['user_id'])

def check_if_user_has_character(user_id, char_id):
    has_char = select_query.select_char_fields(user_id, char_id, ("Character_ID",))

    if has_char is not None:
        return True

    return False

def is_verified():
    _user_data = select_query.select_user_data_from_id(session["user_id"])
    if _user_data is None:
        return False

    return _user_data["Is_Verified"] > 0

def not_verified_redirect():
    return render_template('auth/not_verified.html',
                           header_text="Leone",
                           inner_text=None)

def has_agreed_tos():
    _has_agreed = select_query.get_has_agreed_to_tos(session["user_id"])
    if _has_agreed is None:
        return False

    return _has_agreed > 0

def not_agreed_redirect():
    return redirect(url_for('auth.register_tos'))
