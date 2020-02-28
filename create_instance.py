import os

if not os.path.exists('/example_site_data/instance'):
	os.makedirs('/example_site_data/instance/database')
	os.makedirs('/example_site_data/instance/uploads/items')
	os.makedirs('/example_site_data/instance/uploads/users')

	#os.execl('/bin/python3', 'python3', '/var/www/src/')