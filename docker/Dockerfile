# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
LABEL org.opencontainers.image.authors="Danny Nielsen & Kim Meyer Albrechtsen"
SHELL ["/bin/bash", "-c"] 
ENV DEBIAN_FRONTEND noninteractive

ADD ./start.sh start.sh

# Install misc. dependencies using APT
RUN apt-get update && apt-get install -y \
    git
    #wget \
    #lsb-release \ 
    #gnupg \
    # mariadb-server

# Fetch dIC source code
RUN git clone https://github.com/dbdness/dnikma-thesis-2021.git
# RUN git clone --single-branch --branch demo https://github.com/dbdness/dnikma-thesis-2021.git
WORKDIR /dnikma-thesis-2021/

# Install MySQL
RUN wget https://dev.mysql.com/get/mysql-apt-config_0.8.17-1_all.deb
    #debconf-set-selections <<< "mysql-community-server mysql-community-server/root-pass password mypassword" && \
    #debconf-set-selections <<< "mysql-community-server mysql-community-server/re-root-pass password mypassword" && \
RUN dpkg -i mysql-apt-config* && \ 
     apt-get update && \ 
     apt-get -y install mysql-server

# mysql -u root -t < infrastructure/norhwind/northwind-nofks-setup.sql
#RUN mysqld && mysql -u root -t < infrastructure/norhwind/northwind-nofks-setup.sql 
# Setup MySQL databses: northwind_nofks and Sakila
# RUN /etc/init.d/mysql start && mysql -u root -t < infrastructure/norhwind/northwind-nofks-setup.sql && mysql -u root -t < infrastructure/sakila/sakila-dic-schema.sql && mysql -u root -t < infrastructure/sakila/sakila-dic-data.sql

# Install dIC
RUN pip install -e .

CMD ["/bin/bash", "/start.sh"]