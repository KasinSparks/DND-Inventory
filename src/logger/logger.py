from colorama import Fore
import os
from datetime import datetime



class Logger:
	def __init__(self, enabled=True, timestamp=True):
		self.enabled = enabled
		self._errorPrefix = 'ERROR: '
		self.timestamp = timestamp

	def log(self, message, color=Fore.GREEN):
		m = str(message)

		if self.timestamp:
			m = self._dateToStringFormat(datetime.now()) + m

		print(color + m)
	
	def error(self, message):
		self.log(self._errorPrefix + str(message), Fore.RED)

	def logToFile(self, message, file):
		try:
			with open(file, 'a+') as f:
				m = str(message)

				if self.timestamp:
					m = self._dateToStringFormat(datetime.now()) + m

				f.write(m + '\n')
		except FileNotFoundError:
			self.error(str(file) + ' not found.')
			return
		except PermissionError:
			self.error('Invalid permissions for ' + str(file))
			return
	
	def logErrorToFile(self, message, file):
		self.logToFile(self._errorPrefix + str(message), file)

	def _dateToStringFormat(self, dt : datetime = None):
		if dt is None:
			d = datetime.now()
		else:
			d = dt

		datetimeString = '[' + str(d.year) + '.' + str(d.month) + '.' + str(d.day) + ' ' + str(d.hour) + ':' + str(d.minute) + ':' + str(d.second) + '] '
		return datetimeString 

		
		

