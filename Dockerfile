FROM ubuntu:latest

COPY ./ /DND-Inventory
VOLUME /site_data

RUN chmod 750 /DND-Inventory/install

EXPOSE 80
EXPOSE 443
