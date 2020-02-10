import base64

def convert_image_to_base64(image_path : str):
	extention = image_path.split('.')[-1]
	with open(image_path, 'rb') as image:
		return {'image_type' : extention, 'encoded_image': base64.b64encode(image.read()).decode('utf-8') }

