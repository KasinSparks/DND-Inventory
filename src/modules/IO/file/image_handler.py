from logger.logger import Logger

from execptions.FileNotSuppliedException import FileNotSuppliedException

from werkzeug.utils import secure_filename

from flask import current_app, session

from PIL import Image

import os

import datetime

class ImageHandler():
    def __init__(self):
        self._logger = Logger()

    def save_image(self, image, save_dir_name, filename=None):
        try:
            if image is None or image.filename == '':
                raise(FileNotSuppliedException('No file name found for the image. (File name was blank)'))

            if self._allowed_file(image.filename):
                image_name = self._append_date_to_filename(secure_filename(image.filename))
                if filename is not None:
                    image_name = secure_filename(filename + '.' + image.filename.split('.')[-1])

                if not os.path.exists(save_dir_name):
                    os.makedirs(save_dir_name, mode=0o770)
                    

                image.save(os.path.join(save_dir_name, image_name))
                return image_name 
        except FileNotSuppliedException as e:
            self._logger.error("save_image function encountered an error... " + str(e.value))
        except Exception:
            self._logger.error("Invalid file, could not save.")

        return None 

    def _append_date_to_filename(self, filename):
        cur_time = datetime.datetime.utcnow()
        extention = filename.split('.')[1]
        temp_filename = filename[0:(len(filename) - len(extention) - 1)]
        temp_filename += "_" + str(cur_time.day) + str(cur_time.month) + \
            str(cur_time.year) + str(cur_time.hour) + str(cur_time.minute) + \
            str(cur_time.second) + str(cur_time.microsecond) + '.' + extention
        return temp_filename

    def _allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

    def _resize_image_to_thumbnail(self, path, new_size=(64,64), save_path="", new_file_name=""):
        full_dir = os.path.split(path)
        directory = full_dir[0]
        existing_file_name = full_dir[1].split('.')[0]

        if save_path == "":
            save_path = directory 

        new_file = secure_filename(existing_file_name + "_thumbnail" + ".png")
        if new_file_name != "":
            new_file = secure_filename(new_file_name + "_thumbnail" + ".png")

        try:
            image = Image.open(path)

            if new_size[0] == new_size[1]:
                image = self._crop_to_square(image)

            image.thumbnail(new_size)
            new_path = os.path.join(save_path, new_file)
            image.save(new_path, "png")
            return new_file
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
