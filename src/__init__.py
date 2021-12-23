import os

from flask import Flask, render_template, session, send_from_directory, request, redirect, url_for

def create_app(test_config=None, is_development_env=True, instance_path=None):
    # create and configure the app
    if instance_path is None:
        app = Flask(__name__, instance_relative_config=True)
    else:
        app = Flask(__name__, instance_path=str(instance_path))

    config_filename = 'production'
    if is_development_env:
        config_filename = 'debug'
    # get the app's config
    app.config.from_json(os.path.join(app.instance_path, config_filename + '.cfg'))

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # database
    from modules.data.database.db import init_app
    init_app(app)

    #---------------------------------------------------------------#
    #                        Blueprints                             #
    #---------------------------------------------------------------#
    # auth
    from blueprints import auth
    app.register_blueprint(auth.bp)
    # data_server
    from blueprints import data_server
    app.register_blueprint(data_server.bp)
    # character
    from blueprints import character
    app.register_blueprint(character.bp)
    # admin
    from blueprints import admin
    app.register_blueprint(admin.bp)
    # image_server
    from blueprints import image_server
    app.register_blueprint(image_server.bp)
    # creation kit
    from blueprints import tools
    app.register_blueprint(tools.bp)



    from blueprints.auth import login_required, get_current_username

    from modules.account.authentication_checks import is_admin

    @app.route('/')
    @app.route('/home')
    @login_required
    def home():
        from modules.data.database.query_modules import select_query
        from modules.account.authentication_checks import is_verified, not_verified_redirect, has_agreed_tos, not_agreed_redirect

        if not is_verified():
            return not_verified_redirect()
        if not has_agreed_tos():
            return not_agreed_redirect()


        header_text = get_current_username()

        site_notifications = select_query.select_site_notifications()
        if site_notifications is None or len(site_notifications) < 1:
            site_notifications = None

        if is_admin():
            return render_template('auth/admin.html',
                                   header_text=header_text,
                                   unread=False,
                                   site_notification=site_notifications)


        return render_template('auth/user.html',
                               header_text=header_text,
                               site_notification=site_notifications)

    @app.route("/robots.txt")
    def robots():
        return send_from_directory(app.static_folder, request.path[1:])

    return app
