FROM ubuntu:latest

RUN adduser dnd

COPY ./ /home/dnd/DND-Inventory
VOLUME /home/dnd/site_data

RUN chmod 750 /home/dnd/DND-Inventory/install

EXPOSE 80
EXPOSE 443
