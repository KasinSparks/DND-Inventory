FROM ubuntu:19.10
RUN apt update && apt install -y \
    apache2 python3 python3-pip libapache2-mod-wsgi-py3 sqlite3

COPY ./requirements.txt /tmp/
RUN pip3 install --requirement /tmp/requirements.txt

COPY ./src /var/www/src
COPY ./run.wsgi /var/www/src/
COPY ./install /tmp/

COPY ./apache2_site.conf /etc/apache2/sites-available/

VOLUME /site_data

COPY ./create_instance.py /tmp/
COPY ./example.cfg /tmp/
COPY ./schema.sql /tmp/


RUN python3 /tmp/create_instance.py && \
    sqlite3 /example_site_data/instance/database/db.sqlite < /tmp/schema.sql && \
    chown -R www-data /example_site_data/instance/database && \
    chown -R www-data /example_site_data/instance/uploads && \
	chmod 750 /tmp/install && \
    cp /tmp/example.cfg /example_site_data/instance/production.cfg && \
    service apache2 start && \ 
    a2dissite 000-default && \ 
    a2ensite apache2_site && \
    service apache2 reload


EXPOSE 80
EXPOSE 443
