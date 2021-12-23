import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

import datetime

from modules.account.account_try import add_account_try, account_tries_remaining, get_lockout_time, is_attempt_within_range
from modules.data.form_data import get_request_field_data
from modules.data.database.query_modules import select_query, insert_query, update_query
from modules.account.authentication_checks import is_verified, not_verified_redirect, has_agreed_tos, not_agreed_redirect

import math

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Register
@bp.route('/register', methods=('GET', 'POST'))
def register():
    header_text = 'Register'
    error = None
    username = ""

    if request.method == 'POST':
        username = get_request_field_data('username')
        password = get_request_field_data('password')
        confirm_password = get_request_field_data('password_confirm')
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif password != confirm_password:
            error = 'Passwords do not match.'
        elif len(username) > 15:
            error = 'Username MAX 15 characters'
        elif select_query.get_user_id(username) is not None:
            error = '{} Taken.'.format(username)

        if error is None:
            insert_query.create_user(username, generate_password_hash(password))
            session.clear()
            session['user_id'] = select_query.get_user_id(username)
            return redirect(url_for('auth.register_tos'))

        flash(error)

    return render_template('auth/register.html',
                           header_text=header_text,
                           error_msg=error,
                           username=username)

# Login
@bp.route('/login', methods=('GET', 'POST'))
def login():
    header_text = 'Leone'
    tries_remaining = 0
    unlockout_time = {}
    error = None

    if request.method == 'POST':
        username = get_request_field_data('username')
        password = get_request_field_data('password')
        user = select_query.select_user_data(username)

        if user is not None:

            timeout_time_minutes = 10

            if account_tries_remaining(user['User_ID']) < 1 and is_attempt_within_range(user['User_ID'], timeout_time_minutes):
                # Accout locked
                # TODO: clean up
                tries_remaining = 0
                lockout_time = get_lockout_time(user['User_ID'])
                time_until_unlocked = ((datetime.timedelta(minutes=timeout_time_minutes) + lockout_time) - datetime.datetime.utcnow())
                time_until_unlocked_minutes = math.trunc(time_until_unlocked.seconds / 60)
                time_until_unlocked_seconds = time_until_unlocked.seconds % 60
                unlockout_time = {'Minutes' : time_until_unlocked_minutes, 'Seconds' : time_until_unlocked_seconds}
                error = 'Account Locked'
            elif not check_password_hash(user['Password'], password):
                error = 'Incorrect password'
                tries_remaining = add_account_try(user['User_ID'], timeout_time_minutes)['tries_remaining']
        else:
            error = 'Incorrect login'


        if error is None:
            session.clear()
            session['user_id'] = user['User_ID']

            # Check for TOS agreement
            has_agreed_tos = select_query.get_has_agreed_to_tos(session['user_id'])
            if has_agreed_tos < 1:
                # User has not agreed
                return redirect(url_for('auth.register_tos'))

            # Check for is verified
            if user['Is_Verified'] < 1:
                return render_template('auth/not_verified.html',
                                       header_text=header_text,
                                       inner_text=None)

            return redirect(url_for('home'))

        flash(error)

    site_notifications = select_query.select_site_notifications()
    if site_notifications is None or len(site_notifications) < 1:
        site_notifications = None

    return render_template('auth/login.html',
                           header_text=header_text,
                           error_msg=error,
                           tries_remaining=tries_remaining,
                           unlockout_time=unlockout_time,
                           site_notification=site_notifications)

# Check if user is already loged in before a request
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = select_query.select_user_data_from_id(user_id)

# Logout
@bp.route('/logout')
def logout():
    session.clear()
    #return redirect(url_for('index'))
    return redirect(url_for('auth.login'))

# Authentication required
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view

def verified_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not is_verified():
            return not_verified_redirect()
        return view(**kwargs)

    return wrapped_view

def tos_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not has_agreed_tos():
            return not_agreed_redirect()
        return view(**kwargs)

    return wrapped_view

@bp.route('/register/tos')
@login_required
def register_tos():
    # TODO: if user has already accepted TOS
    return render_template('auth/register_tos.html',
                            header_text=get_current_username())

@bp.route('/register/tos/accept')
@login_required
def accept_tos():
    # If user has already accepted
    has_accepted = select_query.get_has_agreed_to_tos(session['user_id'])

    if has_accepted > 0:
        # User has already accepted the TOS
        return render_template('auth/accepted_tos.html',
                                header_text=get_current_username(),
                                inner_text='You have already accepted the Terms of Service')

    notification_type = select_query.get_notification_id("New User")

    # Generate admin notification
    insert_query.create_admin_notification(session['user_id'], notification_type)

    # Update user info in DB
    update_query.update_tos_agreement(session['user_id'], True)

    # Get the user name
    username = select_query.get_username(session['user_id'])

    # Redirect to next screen
    return render_template('auth/accepted_tos.html',
                            header_text=get_current_username(),
                            inner_text=None,
                            username=username)

@login_required
def get_current_username():
    return select_query.get_username(session['user_id'])

# Depercated
"""@login_required
def is_verifed():
    user_data = select_query.select_user_data_from_id(session["user_id"])
    if user_data is not None and user_data["Is_Verified"] > 0:
        return True

    return False
"""

def get_current_user_id():
    return session['user_id']