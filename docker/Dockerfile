# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
LABEL org.opencontainers.image.authors="Danny Nielsen & Kim Meyer Albrechtsen"

# Adding startup script to the image
ADD ./start.sh start.sh

# Install dependencies using APT
RUN apt-get update && apt-get install -y \
    git \ 
    mariadb-server

# Install dIC
RUN git clone https://github.com/dbdness/dnikma-thesis-2021.git
WORKDIR /dnikma-thesis-2021/
RUN pip install -e .

# Execute startup script as entrypoint
CMD ["/bin/bash", "/start.sh"]