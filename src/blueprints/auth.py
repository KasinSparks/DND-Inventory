import functools

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from ..db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Register
@bp.route('/register', methods=('GET', 'POST'))
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None

		if not username:
			error = 'Username is required.'
		elif not password:
			error = 'Password is required.'
		elif db.execute(
			# TODO
			'SELECT User_ID FROM Users WHERE Username = ?', (username,)
		).fetchone() is not None:
			error = 'User {} is already registered.'.format(username)

		if error is None:
			db.execute(
				# TODO
				'INSERT INTO user (Username, Password) VALUES (?, ?)',
				(username, generate_password_hash(password))
			)
			db.commit()
			return redirect(url_for('auth.login'))

		flash(error)

	return render_template('auth/register.html')

# Login
@bp.route('/login', methods=('GET', 'POST'))
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None
		user = db.execute(
			# TODO
			'SELECT * FROM Users WHERE Username = ?', (username,)
		).fetchone()

		if user is None or not check_password_hash(user['Password'], password):
			error = 'Incorrect login info.'

		if error is None:
			session.clear()
			session['user_id'] = user['ID']
			# TODO
			#return redirect(url_for('index'))
			return redirect(url_for('home'))

		flash(error)

	return render_template('auth/login.html')

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


