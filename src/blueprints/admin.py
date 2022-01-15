import os

from flask import (
    Blueprint, g, redirect, render_template, request, session, url_for, current_app, jsonify
)

from werkzeug.utils import secure_filename
from blueprints.auth import login_required, get_current_username, tos_required, verified_required
from modules.data.database.query_modules import select_query, delete_query, insert_query, update_query
from modules.account.authentication_checks import is_admin, not_admin_redirect
from modules.data.string_shorten import shorten_string
from modules.data.form_data import get_request_field_data, convert_form_field_data_to_int
from modules.IO.file.image_handler import ImageHandler
from logger.logger import Logger

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('users')
@login_required
@tos_required
@verified_required
def admin_users():
    if not is_admin():
        return not_admin_redirect()

    users = select_query.select_user_data_except_user(session['user_id'])
    user_data = []

    for u in users:
        user_data.append(
            {
                'User_ID' : u['User_ID'],
                'Username' : shorten_string(u['Username'], 16),
                'Is_Verified' : u['Is_Verified'],
                'Is_Admin' : u['Is_Admin']
            }
        )

    return render_template('admin/users.html',
                           users=user_data,
                           header_text=get_current_username())

@bp.route('users/<string:username>')
@login_required
@tos_required
@verified_required
def admin_users_characters(username):
    if not is_admin():
        return not_admin_redirect()

    user_id = select_query.get_user_id(username)
    characters = select_query.select_char_name_and_id(user_id)

    return render_template('admin/characters.html',
                           characters=characters,
                           header_text=get_current_username())


@bp.route('users/verify/<int:user_id>')
@login_required
@tos_required
@verified_required
def admin_verify_user(user_id):
    if not is_admin():
        return not_admin_redirect()
    update_query.update_isVerified(user_id, True)
    return '200'

@bp.route('notifications')
@login_required
@tos_required
@verified_required
def admin_notifications():
    if not is_admin():
        return not_admin_redirect()
    notifications = select_query.select_notifications()

    return render_template('admin/notifications.html',
                           header_text=get_current_username(),
                           notifications=notifications)

@bp.route('notifications/remove/<int:notification_id>')
@login_required
@tos_required
@verified_required
def admin_remove_notification(notification_id):
    if not is_admin():
        return not_admin_redirect()
    delete_query.delete_notification(notification_id)
    return '200'

@bp.route('notifications/markRead/<int:notification_id>')
@login_required
@tos_required
@verified_required
def admin_markRead_notification(notification_id):
    if not is_admin():
        return not_admin_redirect()
    update_query.update_notification_read_status(notification_id, True)
    return '200'

@bp.route('items/approveItem/<int:item_id>/<int:status>')
@login_required
@tos_required
@verified_required
def admin_approve_item_notification(item_id, status):
    if not is_admin():
        return not_admin_redirect()
    
    #q = select_query.select(("Item_ID",), "Admin_Notifications", False, "WHERE Note_ID=?", (notification_id,))
    #item_id = q['Item_ID']
    if status != 0:
        update_query.update_approved_item_status(item_id, True)
    else:
        update_query.update_approved_item_status(item_id, False)
    #delete_query.delete_notification(notification_id)
    return '200'


@bp.route('users/remove', methods=('GET', 'POST'))
@login_required
@tos_required
@verified_required
def admin_remove_user():
    if not is_admin():
        return not_admin_redirect()
    if request.method != 'POST':
        return '400'

    user_id = get_request_field_data('user_id')
    Logger().log("Deleting user with id=" + str(user_id))

    delete_query.delete_user(user_id)

    characters = select_query.get_char_id(user_id)

    for c in characters:
        char_id = c['Character_ID']

        delete_query.delete_character_abilites(char_id)
        delete_query.delete_character_skill(char_id)
        delete_query.delete_character_inventory(char_id)


    delete_query.delete_users_characters(user_id)
    delete_query.delete_login_attempts(user_id)
    delete_query.delete_users_notifications(user_id)

    return '200'

@bp.route('users/makeAdmin', methods=('GET', 'POST'))
@login_required
@tos_required
@verified_required
def make_user_admin():
    if not is_admin():
        return not_admin_redirect()

    if request.method != 'POST':
        return '400'

    user_id = get_request_field_data('user_id')

    update_query.change_user_admin_status(user_id, True)
    Logger().log("User with id=" + str(user_id) + " is now admin")

    return '200'
