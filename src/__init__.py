import os

from flask import Flask, render_template

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

	# a simple page that says hello
	@app.route('/hello')
	def hello():
		return 'Hello, World!'

	@app.route('/')
	@app.route('/home')
	def home():
		return 'Change this later'
	

	return app