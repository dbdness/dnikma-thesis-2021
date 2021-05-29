# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
LABEL org.opencontainers.image.authors="Danny Nielsen & Kim Meyer Albrechtsen"

# Adding startup script to the image
ADD ./start.sh start.sh

# Install dependencies using APT
RUN apt-get update && apt-get install -y \
    git \ 
    mariadb-server

# Pull latest source and install dIC
RUN git clone https://github.com/dbdness/dnikma-thesis-2021.git
WORKDIR /dnikma-thesis-2021/
RUN pip install -e .

# Import sample MySQL databases and create demo user 
RUN /usr/bin/mysqld_safe & sleep 1 && \
    mysql -u root -t < infrastructure/norhwind/northwind-nofks-setup.sql && \
    mysql -u root -t < infrastructure/sakila/sakila-dic-schema.sql && mysql -u root -t < infrastructure/sakila/sakila-dic-data.sql && \
    mysql -u root -e "CREATE USER 'demo'@'localhost' IDENTIFIED BY 'demo'" && \
    mysql -u root -e "GRANT ALL PRIVILEGES ON *.* TO 'demo'@'localhost'"

# Execute startup script as entrypoint
ENTRYPOINT ["/bin/bash", "/start.sh"]