import os

from flask import Flask, render_template, session

def create_app(test_config=None, is_development_env=True, instance_path=None):
	# create and configure the app
	if instance_path is None:
		app = Flask(__name__, instance_relative_config=True)
	else:
		app = Flask(__name__, instance_path=str(instance_path))

	config_filename = 'production'
	if is_development_env:
		config_filename = 'debug'
	# get the app's config	
	app.config.from_json(os.path.join(app.instance_path, config_filename + '.cfg'))

	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	# database
	import db
	db.init_app(app)

	#---------------------------------------------------------------#
	#							Blueprints							#
	#---------------------------------------------------------------#
	
	# auth
	from blueprints import auth
	app.register_blueprint(auth.bp)
	# data_server
	from blueprints import data_server
	app.register_blueprint(data_server.bp)
	# character
	from blueprints import character
	app.register_blueprint(character.bp)
	# admin
	from blueprints import admin 
	app.register_blueprint(admin.bp)


	from blueprints.auth import login_required, get_current_username
	from db import query_db

	@app.route('/')
	@app.route('/home')
	@login_required	
	def home():
		header_text = get_current_username()
		sql_str = """SELECT Is_Admin
				FROM Users 
				WHERE User_ID = ?;
				"""

		isAdmin = query_db(sql_str, (session['user_id'], ), True, True)['Is_Admin']

		if isAdmin > 0:
			#sql_str = """SELECT Has_Been_Read
			#			FROM Admin_Notifications
			#			WHERE Has_Been_Read = 0;
			#		"""	
			#notifications = query_db(sql_str, (), True, True)['Has_Been_Read']

			has_unread = False
			#if notifications is not None:
			#	has_unread = True 

			return render_template('auth/admin.html',
									header_text=header_text,
									unread=has_unread)



		return render_template('auth/user.html',
								header_text=header_text)
	

	return app