import sys
sys.path.insert(0, '/var/www/src')

from __init__ import create_app
application = create_app()
