#!/bin/bash

echo Getting Kong config for from container $1

docker exec -ti $1 /bin/bash -c "kong config db_export /tmp/kong-export.yml"
docker cp $1:/tmp/kong-export.yml ./kong.yml
