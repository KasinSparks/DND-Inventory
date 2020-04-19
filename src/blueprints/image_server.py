from flask import (Blueprint, url_for, send_from_directory, current_app, session)

from blueprints.auth import login_required, verified_required, tos_required

from modules.account.authentication_checks import is_admin
from logger.logger import Logger
from modules.data.database.query_modules import select_query

#from PIL import Image

import os

bp = Blueprint('imageserver', __name__, url_prefix='/imageserver')

@bp.route('/user/<string:image_name>')
@login_required
@verified_required
@tos_required
def getUserImage(image_name):
    image_name_split = str(image_name).split('_')
    if image_name_split[0] != "profile" or image_name_split[1] != "image":
        Logger().error("User image name did not match expected format, profile_image_username_charid_thumbnail")
        return "404"

    user_id = session["user_id"]
    try:
        user_id = select_query.get_user_id(image_name_split[2])
    except:
        Logger().error("Could not find user with the user name: " + str(image_name_split[2]))
        return "404"
    # TODO: Read the docs on how to improve this for server
    path = os.path.join('..', current_app.config['IMAGE_UPLOAD'], 'users', str(user_id), "profile_image")

    return send_from_directory(path, image_name, as_attachment=False)


@bp.route('/item/<string:image_name>')
@login_required
@verified_required
@tos_required
def getItemImage(image_name):
    # TODO: Read the docs on how to improve this for server
    path = os.path.join('..', current_app.config['IMAGE_UPLOAD'], 'items')

    return send_from_directory(path, image_name, as_attachment=False)
