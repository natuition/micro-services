FROM mysql:latest

COPY ./create-table-template.sql /docker-entrypoint-initdb.d/initdb.sql

EXPOSE 3306/tcp
