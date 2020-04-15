from colorama import Fore
from datetime import datetime

class Logger:
    def __init__(self, enabled=True, timestamp=True):
        self.enabled = enabled
        self._ERROR_PREFIX = 'ERROR: '
        self._WARN_PREFIX = 'ERROR: '
        self.timestamp = timestamp
        self._std_color = Fore.WHITE

    def log(self, message, color=Fore.GREEN):
        _m = str(message)

        if self.timestamp:
            _m = self._date_to_string_format(datetime.now()) + _m

        print(color + _m + self._std_color)

    def error(self, message):
        self.log(self._ERROR_PREFIX + str(message), Fore.RED)

    def warning(self, message):
        self.log(self._WARN_PREFIX + str(message), Fore.YELLOW)

    def logToFile(self, message, file):
        try:
            with open(file, 'a+') as f:
                _m = str(message)

                if self.timestamp:
                    _m = self._date_to_string_format(datetime.now()) + _m

                f.write(_m + '\n')
        except FileNotFoundError:
            self.error(str(file) + ' not found.')
            return
        except PermissionError:
            self.error('Invalid permissions for ' + str(file))
            return

    def logErrorToFile(self, message, file):
        self.logToFile(self._ERROR_PREFIX + str(message), file)

    def _date_to_string_format(self, dt : datetime = None):
        if dt is None:
            d = datetime.now()
        else:
            d = dt

        datetimeString = '[' + str(d.year) + '.' + str(d.month) + '.' + str(d.day) + ' ' + str(d.hour) + ':' + str(d.minute) + ':' + str(d.second) + '] '
        return datetimeString
