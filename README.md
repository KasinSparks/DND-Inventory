# DND-Inventory
Character and inventory manager for DND sessions.

# Install / Run
## Start Docker:
0. Change directories to DND-Inventory
1. Run the following commands:

	a) `docker image build --tag=[image_repo_name]:[version.minor_version] .` (do not forget the dot at the end of the command)

	b) `docker container run --name=[container_name] -p [server_port]:80 -it [image_repo_name:version.minor_version]`

2. Proceed to section "Config Webserver"
3. Proceed to section "Start Apache2"
4. Connect by typing, [server_ip]:[server_port], into a web browser
5. Create an account
6. Proceed to section "First Account Verification/Admin"
7. Exit container, but leave container running by pressing ctrl + p then ctrl + q

## Config Webserver:
0. Verify docker container started and you are logged into the container
1. Run the following command (move data folder and change ownership and permissions)

	a.) `/tmp/install`

2. Install a text editor and modify the following fields in '/site_data/instance/production.cfg'

	a.) SECRET_KEY... Look up on Flask website on a good way to generate a secret SECRET_KEY
	
	b.) DATABASE... Change path to where database is located 
	
	c.) IMAGE_UPLOAD... Change path to where image uploads folder is located

3. Modify the ServerName field in the enabled sites (/etc/apache2/sites-enabled/apache2_site.conf) to your server's name

## Start Apache2 (in Docker container):
0. Run the following command(s):

	a.) `service apache2 start`

## First Account Verification/Admin
0. Verify docker container started and you are logged into the container
1. Enter the following commands

	I.) `sqlite3 /site_data/instance/database/db.sqlite "UPDATE Users SET Is_Verified=1, Is_Admin=1 WHERE User_ID=1;"`
