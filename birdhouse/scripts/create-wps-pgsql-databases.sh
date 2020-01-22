#!/bin/bash


docker exec -t postgres psql --username postgres -f /docker-entrypoint-initdb.d/create-wps-databases.sql

