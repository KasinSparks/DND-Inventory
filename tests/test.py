from logger import logger

class Test:
	def __init__(self):
		self.tests = [] 
		self.log = logger.Logger(timestamp=False)

	def runTests(self):
		for t in self.tests:
			try:
				assert t['expected'] == t['actual']
				self.log.log(str(t['name']) + ' Test Passed!')
			except AssertionError:
				self.log.error(
					str(t['name']) + ' Test Failed. Expected: ' +
					str(t['expected']) + ', Received: ' + str(t['actual'])
				)

	def temp(self):
		self.log.logToFile('test', 'testFile')
		self.log.logErrorToFile('test2', 'testFile')


myTest = Test()

myTest.tests.append({
	'name' : 'test0',
	'expected' : 9,
	'actual' : 9
})

myTest.tests.append({
	'name' : 'test1',
	'expected' : 0,
	'actual' : 9
})

myTest.runTests()

myTest.temp()

