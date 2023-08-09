import sys
sys.path.insert(0, '/var/www/src')

from __init__ import create_app
application = create_app(test_config=None, is_development_env=False, instance_path='/site_data/instance')
