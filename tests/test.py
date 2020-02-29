from logger import logger
from logger.logger import Fore

class Test:
	def __init__(self, header_text):
		# Should be an array of dicts
		self.tests = [] 
		self.log = logger.Logger(timestamp=False)
		self.header_text = header_text

	def run_tests(self):
		self.log.log("Beginning test(s) for " + str(self.header_text) + "...", Fore.WHITE)
		count = 1
		passed_count = 0

		for t in self.tests:
			try:
				assert t['expected'] == t['actual']
				self.log.log(self._get_test_block_str(count, t['name']) + '... Test Passed!')
				passed_count += 1
			except AssertionError:
				self.log.log(
					self._get_test_block_str(count, t['name']) + 
					'... Test Failed. Expected: ' +
					str(t['expected']) + ', Received: ' + str(t['actual']), Fore.RED
				)
			count += 1
		
		self.log.log("End of test(s) for " + str(self.header_text) + ".\n", Fore.WHITE)

		# (passed, total)
		return (passed_count, len(self.tests))

	def _get_test_block_str(self, cur_count, test_name):
		test_block_str = "  [Test " + str(cur_count) + " of " + \
						str(len(self.tests)) + "] [" + test_name + "]"
		return test_block_str
