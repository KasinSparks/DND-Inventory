import functools

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

import datetime

from ..db import get_db, query_db

from ..data_obj.account_try import add_account_try, account_tries_remaining, get_lockout_time

import math

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Register
@bp.route('/register', methods=('GET', 'POST'))
def register():
	header_text = 'Register'
	error = None
	username = ""

	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		confirm_password = request.form['password_confirm']
		db = get_db()
		error = None

		if not username:
			error = 'Username is required.'
		elif not password:
			error = 'Password is required.'
		elif password != confirm_password:
			error = 'Passwords do not match.'
		elif len(username) > 15:
			error = 'Username MAX 15 characters'
		elif db.execute(
			# TODO
			'SELECT User_ID FROM Users WHERE Username = ?', (username,)
		).fetchone() is not None:
			error = '{} Taken.'.format(username)

		if error is None:
			db.execute(
				# TODO
				'INSERT INTO Users (Username, Password) VALUES (?, ?)',
				(username, generate_password_hash(password))
			)
			db.commit()

			session.clear()
			session['user_id'] = query_db("SELECT User_ID FROM Users WHERE Username=?", (username,), True, True)['User_ID']

			return redirect(url_for('auth.register_tos'))
			

		flash(error)

	return render_template('auth/register.html',
							header_text=header_text,
							error_msg=error,
							username=username)

# Login
@bp.route('/login', methods=('GET', 'POST'))
def login():
	header_text = 'Site Name Here'
	tries_remaining = 0
	unlockout_time = {}
	error = None

	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		user = db.execute(
			'SELECT * FROM Users WHERE Username = ?', (username,)
		).fetchone()

		if user is not None and account_tries_remaining(user['User_ID']) < 1:
			# Accout locked
			tries_remaining = 0
			lockout_time = get_lockout_time(user['User_ID'])
			time_until_unlocked = ((datetime.timedelta(hours=24) + lockout_time) - datetime.datetime.utcnow())
			time_until_unlocked_hours = math.trunc(time_until_unlocked.seconds / 3600)
			time_until_unlocked_minutes = math.trunc((time_until_unlocked.seconds / 3600 - math.trunc(time_until_unlocked.seconds / 3600)) * 60)
			unlockout_time = {'Hours' : time_until_unlocked_hours, 'Minutes' : time_until_unlocked_minutes}
			error = 'Account Locked'
		elif user is None:
			error = 'Incorrect login'
		elif not check_password_hash(user['Password'], password):
			error = 'Incorrect password'
			tries_remaining = add_account_try(user['User_ID'])['tries_remaining']


		if error is None:
			session.clear()
			session['user_id'] = user['User_ID']
			# TODO
			#return redirect(url_for('index'))

			# Check for TOS agreement
			sql_str = """SELECT Has_Agreed_TOS
						FROM Users
						WHERE User_ID=?;
					"""
			if query_db(sql_str, (session['user_id'],), True, True)['Has_Agreed_TOS'] < 1:
				# User has not agreed
				return redirect(url_for('auth.register_tos'))
		
			return redirect(url_for('home'))

		flash(error)

	return render_template('auth/login.html',
							header_text=header_text,
							error_msg=error,
							tries_remaining=tries_remaining,
							unlockout_time=unlockout_time)



# Check if user is already loged in before a request
@bp.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')

	if user_id is None:
		g.user = None
	else:
		g.user = get_db().execute(
			# TODO
			'SELECT * FROM Users WHERE User_ID = ?', (user_id,)
		).fetchone()

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


@bp.route('/register/tos')
@login_required
def register_tos():
	# TODO: if user has already accepted TOS

	return render_template('auth/register_tos.html',
							header_text='Site Name Here')

@bp.route('/register/tos/accept')
@login_required
def accept_tos():
	# If user has already accepted
	sql_str = """SELECT Has_Agreed_TOS
				FROM Users
				WHERE User_ID=?;
				"""

	has_accepted = query_db(sql_str, (session['user_id'],), True, True)['Has_Agreed_TOS']

	if has_accepted > 0:
		# User has already accepted the TOS
		return render_template('auth/accepted_tos.html',
								header_text='Site Name Here',
								inner_text='You have already accepted the Terms of Service')

	sql_str = """SELECT Notification_ID 
				FROM Notification_Types
				WHERE Type = ?;
				"""

	notification_type = query_db(sql_str, ('New User',), True, True)

	# Generate admin notification
	sql_str = """INSERT INTO Admin_Notifications
				VALUES (?, ?, 0);
				"""

	query_db(sql_str, (session['user_id'], notification_type['Notification_ID'],), False)

	# Update user info in DB
	sql_str = """UPDATE Users
				SET Has_Agreed_TOS = 1
				WHERE User_ID=?;
				"""

	query_db(sql_str, (session['user_id'],), False)

	# Get the user name
	sql_str = """SELECT Username
				From Users
				WHERE User_ID=?;
				"""

	username = query_db(sql_str, (session['user_id'],), True, True)['Username']

	# Redirect to next screen
	return render_template('auth/accepted_tos.html',
							header_text='Site Name Here',
							inner_text=None,
							username=username)