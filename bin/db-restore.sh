#!/bin/bash

source .env
docker-compose exec db pg_restore -c -Fc --dbname=postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@localhost:5432/fajne_dane "/var/lib/backups/$1"

