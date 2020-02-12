import base64

from flask import url_for

from .blueprints.auth import login_required

from PIL import Image

import os

def convert_image_to_base64(image_path : str, scale_to = None):
	try:
		if image_path is None or image_path == '':
			raise Exception('Invaild image')
		return convert_image_helper(image_path, scale_to)
	except:
		return convert_image_helper(os.path.join('src', 'static', 'images', 'no_image.png'), scale_to)
	


def convert_image_helper(image_path : str, scale_to):
	extention = image_path.split('.')[-1]

	#im = Image.open(image_path)
		#thumbnail = im.thumbnail(scale_to, Image.ANTIALIAS)
	#thumbnail = im.resize((100,100))

#	print(thumbnail)

	with open(image_path, 'rb') as image:
		return {'image_type' : extention, 'encoded_image': base64.b64encode(image.read()).decode('utf-8') }
#	return {'image_type' : extention, 'encoded_image': base64.b64encode(thumbnail.stream()).decode('utf-8') }

