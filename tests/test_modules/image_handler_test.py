from test import Test
from modules import image_handler

from PIL import Image

import os

class ImageHandlerTest(Test):
	def __init__(self):
		super().__init__("Image Hander Test")

		self.tests.append(self._save_image_none())
		self.tests.append(self._save_image_empty())
		self.tests.append(self._allowed_file_empty_string())
		self.tests.append(self._allowed_file_not_allowed())
		self.tests.append(self._allowed_file_allowed())
		self.tests.append(self._save_image_test())
		self.tests.append(self._get_image_size_test())
		self.tests.append(self._largest_square_size_test(256, "no_image.png"))
		self.tests.append(self._largest_square_size_test(682, "Tree.jpg"))
		self.tests.append(self._largest_square_test((0,0,256,256), "no_image.png"))
		self.tests.append(self._largest_square_test((171,0,853,682), "Tree.jpg"))
		self.tests.append(self._crop_to_square_test("no_image.png"))
		self.tests.append(self._crop_to_square_test("Tree.jpg"))




	def _save_image_none(self):
		handler = image_handler.ImageHandler()
		results = {
			"name" : "Save None Image",
			"expected" : -1,
			"actual" : handler.save_image(None, "")
		}
		return results 

	def _save_image_empty(self):
		handler = image_handler.ImageHandler()
		results = {
			"name" : "Save Empty String as Image",
			"expected" : -2,
			"actual" : handler.save_image("", "")
		}
		return results 

	def _allowed_file_empty_string(self):
		handler = image_handler.ImageHandler()
		results = {
			"name" : "Empty String in Allowed File",
			"expected" : False,
			"actual" : handler._allowed_file("")
		}
		return results 

		
	def _allowed_file_not_allowed(self):
		handler = image_handler.ImageHandler()
		results = {
			"name" : "Not Allowed File Extention",
			"expected" : False,
			"actual" : handler._allowed_file("test.asdf")
		}
		return results 

	def _allowed_file_allowed(self):
		handler = image_handler.ImageHandler()
		results = {
			"name" : "Allowed File Extention",
			"expected" : True,
			"actual" : handler._allowed_file("test.png")
		}
		return results 

		
	def _save_image_test(self):
		handler = image_handler.ImageHandler()
		save_dir = os.path.join(self._get_test_image_dir(), "temp")


		results = {
			"name" : "Save Image Test",
			"expected" : 1,
			"actual" : handler.save_image(self._get_test_image(), save_dir)
		}

		self._clean_temp_folder(save_dir)

		return results 

	def _get_image_size_test(self):
		handler = image_handler.ImageHandler()
		results = {
			"name" : "Image Size",
			"expected" : (256,256),
			"actual" : handler._get_image_size(self._get_test_image())
		}
		return results

	def _largest_square_size_test(self, size, image_filename="no_image.png"):
		handler = image_handler.ImageHandler()
		img_size = handler._get_image_size(self._get_test_image(image_filename))
		results = {
			"name" : "Largest Square Size",
			"expected" : size,
			"actual" : handler._largest_square_size(img_size)
		}	
		return results

	def _largest_square_test(self, lis, image_filename="no_image.png"):
		handler = image_handler.ImageHandler()
		size = handler._get_image_size(self._get_test_image(image_filename))
		results = {
			"name" : "Largest Square",
			"expected" : lis,
			"actual" : handler._largest_square(size)
		}	
		return results

	def _crop_to_square_test(self, image_filename="no_image.png"):
		handler = image_handler.ImageHandler()
		original_img_size = handler._get_image_size(self._get_test_image(image_filename))
		s = handler._largest_square_size(original_img_size)
		cropped_img = handler._crop_to_square(self._get_test_image(image_filename))
		results = {
			"name" : "Crop To Square",
			"expected" : (s,s),
			"actual" : handler._get_image_size(cropped_img)
		}	
		return results


	def _get_test_image(self, filename="no_image.png"):
		image_dir = self._get_test_image_dir()
		image = os.path.join(image_dir, filename)
		return Image.open(image)



	def _get_test_image_dir(self):
		return os.path.abspath(os.path.join("tests", "test_assests")) 


	def _clean_temp_folder(self, temp_dir):
		current_dir = os.path.split(temp_dir)
		parent_dir = os.path.split(current_dir[0])

		if current_dir[1] != "temp" or parent_dir[1] != "test_assests":
			return

		for f in os.listdir(temp_dir):
			os.remove(os.path.join(temp_dir, f))
