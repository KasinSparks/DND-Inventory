from flask import (Blueprint, url_for, send_from_directory, current_app, session)

from blueprints.auth import login_required

from modules.account.authentication_checks import is_admin

#from PIL import Image

import os

bp = Blueprint('imageserver', __name__, url_prefix='/imageserver')

@bp.route('/user/<string:image_name>')
@login_required
def getUserImage(image_name):
	# TODO: Read the docs on how to improve this for server
	path = os.path.join('..', current_app.config['IMAGE_UPLOAD'], 'users', str(session['user_id']), "profile_image")
	
	return send_from_directory(path, image_name, as_attachment=False)
	

@bp.route('/item/<string:image_name>')
@login_required
def getItemImage(image_name):
	# TODO: Read the docs on how to improve this for server
	path = os.path.join('..', current_app.config['IMAGE_UPLOAD'], 'items')

	return send_from_directory(path, image_name, as_attachment=False)
