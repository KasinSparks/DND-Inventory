import os

if not os.path.exists('/site_data/instance'):
	os.makedirs('/site_data/instance/database')
	os.makedirs('/site_data/instance/uploads/items')
	os.makedirs('/site_data/instance/uploads/users')

	#os.execl('/bin/python3', 'python3', '/var/www/src/')