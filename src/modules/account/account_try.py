import datetime
from modules.data.database.db import query_db

def add_account_try(user_id):

	tries_remaing = check_try_attempts(user_id)

	update_sql_str = """UPDATE Login_Attempts
						SET Number_Attempts = ?, Attempt_Year = ?, Attempt_Month = ?, Attempt_Day = ?, Attempt_Hour = ?, Attempt_Minute = ?, Attempt_Second = ?
						WHERE User_ID = ?;
						""" 

	if tries_remaing < 1:
		tries_remaing = 0
	else:
		tries_remaing -= 1

	current_time = datetime.datetime.utcnow()

	num_of_attempts = __get_number_of_attempts__(user_id) + 1

	query_db(update_sql_str, (num_of_attempts, current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute, current_time.second, user_id,), False)

	result = {'tries_remaining' : tries_remaing, 'locked_time' : current_time}

	return result

def check_try_attempts(user_id):
	# check number of attempts
	tries = account_tries_remaining(user_id)
	if tries < 1:
		# see if tries need to be reset
		if not is_attempt_within_range(user_id):
			# reset tries
			reset_tries_sql_str = """UPDATE Login_Attempts
									SET Number_Attempts = 0
									WHERE User_ID = ?;
								"""
			query_db(reset_tries_sql_str, (user_id,), False)
	
	return tries 


def account_tries_remaining(user_id):
	# Query DB for login attempts
	#  if 3 attempts have been tried within a given hour period,
	#  account is locked, else return number of tries remaining
	return 3 - __get_number_of_attempts__(user_id)

def get_lockout_time(user_id):
	attempt_data = __get_attempt_data__(user_id)
	attempt_datetime = datetime.datetime(attempt_data['Attempt_Year'], attempt_data['Attempt_Month'], attempt_data['Attempt_Day'], attempt_data['Attempt_Hour'], attempt_data['Attempt_Minute'], attempt_data['Attempt_Second'])
	return attempt_datetime 

# range is measured within hours
def	is_attempt_within_range(user_id, range=24):
	result = __get_attempt_data__(user_id)

	if result is None:
		print("ERROR: No results...")

	current_datetime = datetime.datetime.utcnow()
	attempt_datetime = datetime.datetime(result['Attempt_Year'], result['Attempt_Month'], result['Attempt_Day'], result['Attempt_Hour'], result['Attempt_Minute'], result['Attempt_Second'])

	diff_seconds = (current_datetime - attempt_datetime).seconds

	print('Diffrence in seconds: {}'.format(diff_seconds))

	diff_hours = (diff_seconds / 3600)	

	if diff_hours > range:
		return True

	return False

def create_login_attempt(user_id):
	query_str = """INSERT INTO Login_Attempts (User_ID)
					VALUES (?);
				"""
	query_db(query_str, (user_id,), False)

	return



def __get_number_of_attempts__(user_id):
	query_str = """SELECT Number_Attempts FROM Login_Attempts
					WHERE User_ID = ?;
				"""
	query_result = query_db(query_str, (user_id,), True, True)

	result = None	
	if query_result is not None:
		result = query_result['Number_Attempts']
	else:
		create_login_attempt(user_id)
		result = 0
	
	return int(result)


def __get_attempt_data__(user_id):
	query_str = """SELECT Attempt_Year, Attempt_Month, Attempt_Day, Attempt_Hour, Attempt_Minute, Attempt_Second FROM Login_Attempts
					WHERE User_ID = ?;
				"""
	query_result = query_db(query_str, (user_id,), True, True)

	result = None
	if query_result is not None:
		result = dict(query_result)
	else:
		raise Exception('ERROR: No login attempt record in DB...')	

	return result
