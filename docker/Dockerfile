# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
LABEL org.opencontainers.image.authors="Danny Nielsen & Kim Meyer Albrechtsen"

# Adding startup script to the image
ADD ./start.sh start.sh

# Install misc. dependencies using APT
RUN apt-get update && apt-get install -y \
    git \ 
    mariadb-server

# Fetch dIC source
RUN git clone https://github.com/dbdness/dnikma-thesis-2021.git
WORKDIR /dnikma-thesis-2021/

# Install dIC
RUN pip install -e .

CMD ["/bin/bash", "/start.sh"]