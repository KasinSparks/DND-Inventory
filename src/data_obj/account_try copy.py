import datetime
from ..db import query_db

def add_account_try(user_id, datetime):
	# find oldest try
	oldest = get_oldest_try(user_id)

	# replace or insert
	if oldest is None:
		# insert
		insert_sql_str = """INSERT INTO Attempt (Year, Month, Day, Hour, Minute)
							VALUES(?,?,?,?,?)
						"""

		update_sql_str = """UPDATE Login_Attempts
							SET """ + oldest
	else:
		# replace

	return

def get_oldest_try(user_id):
	result : dict = __get_login_attemptID__(user_id)

	if result is None:
		return None

	oldest = None	
	while oldest is None:
		oldest = __get_attempt_data__(result.popitem()[1])

	if oldest is None:
		# no tries in DB
		return None
	
	#newest = datetime.datetime(temp['Year'], temp['Month'], temp['Day'], temp['Hour'], temp['Minute'])


	for i in result:
		oldest_datetime = datetime.datetime(oldest['Year'], oldest['Month'], oldest['Day'], oldest['Hour'], oldest['Minute'])
		temp = __get_attempt_data__(result[i])
		temp_datetime = datetime.datetime(temp['Year'], temp['Month'], temp['Day'], temp['Hour'], temp['Minute'])
		if (temp_datetime - oldest_datetime).seconds < 0:
			oldest = temp

	return oldest

		


def account_tries_remaining(user_id):
	tries_remaining = 0

	# Query DB for login attempts
	#  if 3 attempts have been tried within a 24 hour period,
	#  account is locked, else return number of tries remaining
	result = __get_login_attemptID__(user_id)

	if result is None:
		return 3

	for i in result:
		if result[i] is None or not is_attempt_within_range(result[i]):
			tries_remaining += 1	

	return tries_remaining

# range is measured within hours
def	is_attempt_within_range(attempt_id, range=24):
	result = __get_attempt_data__(attempt_id)

	if result is None:
		print("ERROR: No results...")

	current_datetime = datetime.datetime.utcnow()
	attempt_datetime = datetime.datetime(result['Year'], result['Month'], result['Day'], result['Hour'], result['Minute'])

	diff_seconds = (current_datetime - attempt_datetime).seconds

	print('Diffrence in seconds: {}'.format(diff_seconds))

	diff_hours = (diff_seconds / 3600)	

	if diff_hours > range:
		return True

	return False

def __get_login_attemptID__(user_id):
	query_str = """SELECT Attempt0_ID, Attempt1_ID, Attempt2_ID FROM Login_Attempts
					WHERE User_ID = ?;
				"""
	query_result = query_db(query_str, (user_id,), True, True)

	result = None	
	if query_result is not None:
		result = dict(query_result)
	
	return result

def __get_attempt_data__(attempt_id):
	query_str = """SELECT * FROM Attempt
					WHERE Attempt_ID = ?;
				"""
	query_result = query_db(query_str, (attempt_id,), True, True)

	result = None
	if query_result is not None:
		result = dict(query_result)

	return result
