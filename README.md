# DND-Inventory
Character and inventory manager for DND sessions.

# Install / Run
Start Docker:
1.) Change directories to DND-Inventory
2.) Run the following commands:
	a) `docker image build --tag=[image_repo_name]:[version.minor_version] .` (do not forget the dot at the end of the command)
	b) `docker container run --name=[container_name] -p [server_port]:[container_port] -it [image_repo_name:version.minor_version]`
3.) Proceed to section "Config Webserver"
4.) Proceed to section "Start Apache2"
5.) Exit container, but leave container running by pressing ctrl + p then ctrl + q
6.) Connect by typing, [server_ip]:[server_port], into a web browser

Config Webserver:
0.) Verify docker container started and you are logged into the container
1.) Use the following command to move files and folders from /example_site_data
	a.) `mv /example_site_data/* /site_data`
2.) Change directories to /site_data
3.) install a text editor and modify the following fields in 'production.cfg'
	a.) SECRET_KEY... Look up on Flask website on a good way to generate a secret SECRET_KEY
	b.) DATABASE... Change path to where database is located 
	c.) IMAGE_UPLOAD... Change path to where image uploads folder is located
4.) modify the ServerName field in the enabled sites (/etc/apache2/sites-enabled/apache2_site.conf) to your server's name
5.) change ownership and permissions
	a.) use the following command to change ownership, 
		I.) `chown www-data -R /site_data/instance/uploads`
		II.) `chown www-data -R /site_data/instance/database`
	b.) use the following command to change permissions, 
		I.) `chmod 740 www-data -R /site_data/instance/uploads`
		II.) `chmod 740 www-data /site_data/instance/database`
		III.) `chmod 740 www-data /site_data/instance/database/database.sqlite`




Start Apache2 (in Docker container):
1.) Run the following command(s)
	a.) `service apache2 start`
