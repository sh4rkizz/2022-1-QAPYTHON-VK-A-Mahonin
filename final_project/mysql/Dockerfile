FROM mysql:latest

WORKDIR .

ADD . /mysql

COPY init.sql /docker-entrypoint-initdb.d/