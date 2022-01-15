import datetime
from modules.data.database.query_modules.update_query import change_num_of_login_attempts, update_attempt_datetime
from modules.data.database.query_modules.select_query import select_attempt_date, get_num_of_login_attempts
from modules.data.database.query_modules.insert_query import create_login_attempt

def add_account_try(user_id, lockout_time_minutes):

    tries_remaing = check_try_attempts(user_id, lockout_time_minutes)

    if tries_remaing < 1:
        tries_remaing = 0
    else:
        tries_remaing -= 1

    num_of_attempts = __get_number_of_attempts__(user_id) + 1
    change_num_of_login_attempts(user_id, num_of_attempts)

    current_time = datetime.datetime.utcnow()
    update_attempt_datetime(user_id, current_time)

    result = {'tries_remaining' : tries_remaing, 'locked_time' : current_time}

    return result

def check_try_attempts(user_id, locked_time_minutes):
    # check number of attempts
    tries = account_tries_remaining(user_id)
    if tries < 1:
        # see if tries need to be reset
        if not is_attempt_within_range(user_id, locked_time_minutes):
            # reset tries
            change_num_of_login_attempts(user_id, 0)
    
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

# range is measured within minutes 
def	is_attempt_within_range(user_id, range=1):
    result = __get_attempt_data__(user_id)

    if result is None:
        print("ERROR: No attempt data results...")

    current_datetime = datetime.datetime.utcnow()
    attempt_datetime = datetime.datetime(result['Attempt_Year'], result['Attempt_Month'], result['Attempt_Day'], result['Attempt_Hour'], result['Attempt_Minute'], result['Attempt_Second'])
    diff_seconds = (current_datetime - attempt_datetime).seconds
    diff_minutes = (diff_seconds / 60)	

    if diff_minutes > range:
        return False 

    return True 

def __get_number_of_attempts__(user_id):
    query_result = get_num_of_login_attempts(user_id)

    result = None	
    if query_result is not None:
        result = query_result['Number_Attempts']
    else:
        create_login_attempt(user_id)
        result = 0
    
    return int(result)

def __get_attempt_data__(user_id):
    query_result = select_attempt_date(user_id)

    if query_result is None:
        raise Exception('ERROR: No login attempt record in DB...')	

    return query_result