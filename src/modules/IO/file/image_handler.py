from logger.logger import Logger

from execptions.FileNotSuppliedException import FileNotSuppliedException

from werkzeug.utils import secure_filename

from flask import current_app, session

from PIL import Image

import os

class ImageHandler():
	def __init__(self):
		self._logger = Logger()

	def save_image(self, image, save_dir_name):
		try:
			if image is None or image.filename == '':
				raise(FileNotSuppliedException('No file name found for the image. (File name was blank)'))

			if self._allowed_file(image.filename):
				filename = secure_filename(image.filename)

				if not os.path.exists(save_dir_name):
					os.mkdir(save_dir_name, mode=0o770)

				image.save(os.path.join(save_dir_name, filename))
			else:
				return -3
		except FileNotSuppliedException as e:
			self._logger.error("save_image function encountered an error... " + str(e.value))
			return -1 
		except Exception:
			self._logger.error("Invalid file, could not save.")
			return -2 

		return 1 

	def _allowed_file(self, filename):
		return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

	def _resize_image_to_thumbnail(self, path, new_size=(64,64), save_path=""):
		full_dir = os.path.split(path)
		directory = full_dir[0]
		existing_file_name = full_dir[1]

		if save_path == "":
			save_path = directory 

		new_file = existing_file_name + ".thumbnail"


		try:
			image = Image.open(path)

			if new_size[0] == new_size[1]:
				image = self._crop_to_square(image)

			image.thumbnail(new_size)
			new_path = os.path.join(directory, new_file)
			image.save(new_path, "png")
			return new_path 
		except IOError as e:
			self._logger.error('Unable to resize image ' + str(existing_file_name) + ' ...\n' + e.strerror)	

		return "" 

	def _get_image_size(self, pil_image):
		return pil_image.size

	def _crop_to_square(self, pil_image):
		ls = self._largest_square(self._get_image_size(pil_image))
		return pil_image.crop(ls)

	def _largest_square_size(self, image_size):
		s = image_size[0]

		# Find the lesser of the two sides
		if image_size[0] > image_size[1]:
			s = image_size[1]

		return s 

	def _largest_square(self, image_size):
		sq_side_len = self._largest_square_size(image_size)

		# Just need one point to set the square's origin
		lp = (image_size[0] - sq_side_len) / 2
		up = (image_size[1] - sq_side_len) / 2

		# (left, upper, right, lowwer) as per pillow docs
		return (lp, up, lp + sq_side_len, up + sq_side_len)
