FROM ubuntu:latest

RUN useradd dnd

COPY ./ /home/dnd/DND-Inventory
VOLUME /home/dnd/site_data

RUN chown dnd -R /home/dnd/DND-Inventory/start && chmod 750 /home/dnd/DND-Inventory/start && chmod 750 /home/dnd/DND-Inventory/install && /home/dnd/DND-Inventory/install


EXPOSE 80
EXPOSE 443
