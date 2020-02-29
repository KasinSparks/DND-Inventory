from logger import logger
from logger.logger import Fore

import flask

from modules import image_handler_test 

class TestRunner():
	def __init__(self):
		self._logger = logger.Logger()
		self._result_queue = []

	def calcluate_results(self):
		num_passed = 0
		num_ran = 0

		for r in self._result_queue:
			num_passed += r[0]
			num_ran += r[1]

		return (num_passed, num_ran)

	def run_tests(self):
		self._result_queue.append(image_handler_test.ImageHandlerTest().run_tests())
	

		results = self.calcluate_results()

		self._logger.log("Test results: " + str(results[0]) + 
								" passed of " + str(results[1]) + " tests ran.", Fore.WHITE)


app = flask.Flask(__name__) 

with app.app_context() as c:
	import os
	app.config.from_json(os.path.join(app.instance_path, 'debug.cfg'))
	TestRunner().run_tests()