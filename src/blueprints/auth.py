import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

import datetime

from modules.account.account_try import add_account_try, account_tries_remaining, get_lockout_time, is_attempt_within_range
from modules.data.form_data import get_request_field_data
from modules.data.database.query_modules import select_query, insert_query, update_query, delete_query
from modules.account.authentication_checks import is_verified, not_verified_redirect, has_agreed_tos, not_agreed_redirect

import math

bp = Blueprint('auth', __name__, url_prefix='/auth')



# Authentication required
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view

def verified_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not is_verified():
            return not_verified_redirect()
        return view(**kwargs)

    return wrapped_view

def tos_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not has_agreed_tos():
            return not_agreed_redirect()
        return view(**kwargs)

    return wrapped_view

@bp.route('/reset')
def reset():
    header_text = 'Reset Password'

    return render_template('auth/reset_getusername.html',
                           header_text=header_text,
                           )


# Reset password
# TODO
@bp.route('/reset/sq', methods=('POST',))
def reset_sq():
    header_text = 'Reset Password'
    error = None
    username = ""

    if request.method == 'POST':
        error = None
        username = get_request_field_data('username')

        if not username:
            error = 'Username is required.'

        if error is not None:
            return redirect(url_for('auth.login'))

        #check to see if user exist and get security questions
        user_id = select_query.get_user_id(username)
        if user_id is None:
            return redirect(url_for('auth.login'))
        
        questions = select_query.select(("Security_Questions.Question", "Security_Questions.ID",), "Users_Security_Questions", True, "WHERE User_ID=?", (user_id,),
                                        ("INNER JOIN Security_Questions ON Users_Security_Questions.Question_ID=Security_Questions.ID",)
        )
        
        num = len(questions)

        return render_template('auth/security_questions_trial.html',
                            header_text=header_text,
                            error_msg=error,
                            num_of_questions=num,
                            questions=questions,
                            username=username
        )

    return render_template('auth/login.html',
                        header_text=header_text,
                        error_msg=error,
    )

@bp.route('/set/newquestions', methods=('POST',))
@login_required
@verified_required
@tos_required
def set_questions():
    header_text = 'Set Security Questions'
    error = None
    # check to make sure the user answered the questions correctly
    if request.method == 'POST':
        username = get_request_field_data('username')

        if username is None or username == "":
            error = 'Username is required'

        user_id = select_query.get_user_id(username)
        if user_id is None:
            error = 'Unknown username' 

        if error is not None:
            print(error)
            return redirect(url_for("auth.login")) 

        #answers = []
        #for r in request.form:
        #    if r[0:6] == 'answer':
        #        answers.append((r[-1], request.form[r]))

        num_of_security_questions = 3
        security_questions = []
        security_answers = []
        for i in range(num_of_security_questions):
            security_questions.append(int(get_request_field_data('security_question' + str(i))))
            security_answers.append(get_request_field_data('answer' + str(i)))


        ## make sure all questions were answered
        for a in security_answers:
            if len(a) < 1 or a == "":
                error = 'Please answer all the security questions.\n'
                break

        memo = []
        for q in security_questions:
            if q < 1:
                error = 'You must select a security question.\n'
                break
            if q in memo:
                error = 'You may not select two or more of the same security question.\n'
                break
            memo.append(q)

        if error is not None:
            defaults = select_query.select(("*",), "Security_Questions", True)
            return render_template('auth/setsecurityquestions.html',
                                    header_text=username,
                                    error_msg=error,
                                    num_of_questions=3,
                                    defaults=defaults,
                                    security_questions=security_questions,
                                    security_answers=security_answers,
                                    username=username
            )

        ## check the password 
        password = get_request_field_data('password')
        if not check_password_hash(select_query.select(("Password",), "Users", False, "WHERE User_ID=?", (user_id,))["Password"], password):
            print("incorrect password")
            return redirect(url_for('auth.login'))

        ## remove old answers
        questions = select_query.select(("Security_Questions.Question", "Security_Questions.ID",), "Users_Security_Questions", True, "WHERE User_ID=?", (user_id,),
                                        ("INNER JOIN Security_Questions ON Users_Security_Questions.Question_ID=Security_Questions.ID",)
        )

        if questions is not None:
            delete_query.delete("Users_Security_Questions", "WHERE User_ID=?", (user_id,))

        ## add new answers
        for i in range(num_of_security_questions):
            insert_query.insert("Users_Security_Questions",
                {
                    "User_ID": user_id,
                    "Question_ID": security_questions[i],
                    "Answer": generate_password_hash(str(security_answers[i]).strip().upper())
                }
            )

        return redirect(url_for("home"))

    error = "Security questions were not set"

    print("here") 
    return render_template('auth/login.html',
                           header_text='Login Page',
                           error_msg=error,
    )


@bp.route('/reset/newpass', methods=('POST',))
def newpass():
    header_text = 'Reset Password'
    error = None
    # check to make sure the user answered the questions correctly
    if request.method == 'POST':
        username = get_request_field_data('username')

        if not username:
            error = 'Username is required'

        user_id = select_query.get_user_id(username)
        if user_id is None:
            error = 'Unknown username' 

        if error is not None:
            return render_template('auth/reset_getusername.html',
                                    header_text='Reset Password',
                                    error_msg=error
            )

        answers = []        
        for r in request.form:
            if r[0:6] == 'answer':
                answers.append((r[-1], request.form[r]))
        

        for a in answers:
            correct_answer = select_query.select(("Answer",), "Users_Security_Questions", False, "WHERE User_ID=? AND Question_ID=?", (user_id, a[0],))
            if not check_password_hash(correct_answer['Answer'], str(a[1]).strip().upper()):
                error = 'Password was not reset'
                break

        password = [get_request_field_data('password'), get_request_field_data('password_confirm')]

        if password[0] != password[1]:
            error = 'Password was not reset'

        if not check_password_requirements(password):
            error = 'Password must be more than ten characters'

        if error is not None:
            return render_template('auth/reset_getusername.html',
                                    header_text='Reset Password',
                                    error_msg=error,
            )

        update_query.update("Users", {"Password": generate_password_hash(password[0])}, "WHERE User_ID=?", (user_id,))
        return render_template('auth/login.html',
                            header_text='Login Page',
                            error_msg=error,
        )

    error = "Password was not reset"
        
    return render_template('auth/login.html',
                           header_text='Login Page',
                           error_msg=error,
    )


def check_password_requirements(password: str) -> str:
    # Passwords need to have the following
    # * at least 10 characters
    # * at least one uppercase and one lowercase
    # * at least one number

    error = "" 

    if (len(password) < 10):
        error += "Password must be more that ten characters.\n"
    ##if (password.islower()):
    ##    error += "Password does not contain at least one uppercase.\n"
    ##if (password.isupper()):
    ##    error += "Password does not contain at least one lowercase.\n"

    return error

# Register
@bp.route('/register', methods=('GET', 'POST'))
def register():
    header_text = 'Register'
    error = "" 
    username = ""
    password = ""
    num_of_security_questions = 3
    security_questions = []
    security_answers = []
    for i in range(num_of_security_questions):
        security_questions.append("")
        security_answers.append("")

    default_security_questions = select_query.select_default_security_questions()

    if request.method == 'POST':
        username = get_request_field_data('username')
        password = get_request_field_data('password')
        security_questions = []
        security_answers = []
        for i in range(num_of_security_questions):
            security_questions.append(int(get_request_field_data('security_question' + str(i))))
            security_answers.append(get_request_field_data('answer' + str(i)))
        confirm_password = get_request_field_data('password_confirm')
        error = "" 

        password_req_check = check_password_requirements(password)

        if not username:
            error += 'Username is required.\n'
        if password_req_check != "":
            error += password_req_check
        if not password:
            error += 'Password is required.\n'
        if password != confirm_password:
            error += 'Passwords do not match.\n'
        if len(username) > 15:
            error += 'Username MAX 15 characters\n'
        if select_query.get_user_id(username) is not None:
            error += '{} Taken.\n'.format(username)
        if len(security_questions) != num_of_security_questions:
            error += 'Please select three of the security questions.\n'
        if len(security_answers) != num_of_security_questions:
            error += 'Please answer all the security questions.\n'

        for a in security_answers:
            if len(a) < 1 or a == "":
                error += 'Please answer all the security questions.\n'
                break

        memo = []
        for q in security_questions:
            if q < 1:
                error += 'You must select a security question.\n'
                break
            if q in memo:
                error += 'You may not select two or more of the same security question.\n'
                break
            memo.append(q)
        


        if error == "":
            insert_query.create_user(username, generate_password_hash(password), security_questions, security_answers)
            session.clear()
            session['user_id'] = select_query.get_user_id(username)
            return redirect(url_for('auth.register_tos'))

        flash(error)

    return render_template('auth/register.html',
                           header_text=header_text,
                           error_msg=error,
                           username=username,
                           password=password,
                           security_questions=security_questions,
                           security_answers=security_answers,
                           defaults=default_security_questions,
                           num_of_questions=num_of_security_questions,)

# Login
@bp.route('/login', methods=('GET', 'POST'))
def login():
    header_text = 'Leone'
    tries_remaining = 0
    unlockout_time = {}
    error = None

    if request.method == 'POST':
        username = get_request_field_data('username')
        password = get_request_field_data('password')
        user = select_query.select_user_data(username)

        if user is not None:

            timeout_time_minutes = 1

            if account_tries_remaining(user['User_ID']) < 1 and is_attempt_within_range(user['User_ID'], timeout_time_minutes):
                # Accout locked
                # TODO: clean up
                tries_remaining = 0
                lockout_time = get_lockout_time(user['User_ID'])
                time_until_unlocked = ((datetime.timedelta(minutes=timeout_time_minutes) + lockout_time) - datetime.datetime.utcnow())
                time_until_unlocked_minutes = math.trunc(time_until_unlocked.seconds / 60)
                time_until_unlocked_seconds = time_until_unlocked.seconds % 60
                unlockout_time = {'Minutes' : time_until_unlocked_minutes, 'Seconds' : time_until_unlocked_seconds}
                error = 'Account Locked'
            elif not check_password_hash(user['Password'], password):
                error = 'Incorrect password'
                tries_remaining = add_account_try(user['User_ID'], timeout_time_minutes)['tries_remaining']
        else:
            error = 'Incorrect login'


        if error is None:
            session.clear()
            session['user_id'] = user['User_ID']

            # Check for TOS agreement
            has_agreed_tos = select_query.get_has_agreed_to_tos(session['user_id'])
            if has_agreed_tos < 1:
                # User has not agreed
                return redirect(url_for('auth.register_tos'))

            # Check for is verified
            if user['Is_Verified'] < 1:
                return render_template('auth/not_verified.html',
                                       header_text=header_text,
                                       inner_text=None)

            return redirect(url_for('home'))

        flash(error)

    site_notifications = select_query.select_site_notifications()
    if site_notifications is None or len(site_notifications) < 1:
        site_notifications = None

    return render_template('auth/login.html',
                           header_text=header_text,
                           error_msg=error,
                           tries_remaining=tries_remaining,
                           unlockout_time=unlockout_time,
                           site_notification=site_notifications)

# Check if user is already loged in before a request
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = select_query.select_user_data_from_id(user_id)

# Logout
@bp.route('/logout')
def logout():
    session.clear()
    #return redirect(url_for('index'))
    return redirect(url_for('auth.login'))

@bp.route('/register/tos')
@login_required
def register_tos():
    # TODO: if user has already accepted TOS
    return render_template('auth/register_tos.html',
                            header_text=get_current_username())

@bp.route('/register/tos/accept')
@login_required
def accept_tos():
    # If user has already accepted
    has_accepted = select_query.get_has_agreed_to_tos(session['user_id'])

    if has_accepted > 0:
        # User has already accepted the TOS
        return render_template('auth/accepted_tos.html',
                                header_text=get_current_username(),
                                inner_text='You have already accepted the Terms of Service')

    notification_type = select_query.get_notification_id("New User")

    # Generate admin notification
    insert_query.create_admin_notification(session['user_id'], notification_type)

    # Update user info in DB
    update_query.update_tos_agreement(session['user_id'], True)

    # Get the user name
    username = select_query.get_username(session['user_id'])

    # Redirect to next screen
    return render_template('auth/accepted_tos.html',
                            header_text=get_current_username(),
                            inner_text=None,
                            username=username)

@login_required
def get_current_username():
    return select_query.get_username(session['user_id'])

# Depercated
"""@login_required
def is_verifed():
    user_data = select_query.select_user_data_from_id(session["user_id"])
    if user_data is not None and user_data["Is_Verified"] > 0:
        return True

    return False
"""

def get_current_user_id():
    return session['user_id']