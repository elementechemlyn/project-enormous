#!/bin/bash

echo Getting Keycloak config for Realm $1 from container $2

docker exec -ti $2 /bin/bash -c "/opt/jboss/keycloak/bin/standalone.sh -Dkeycloak.migration.usersExportStrategy=SAME_FILE -Dkeycloak.migration.action=export -Dkeycloak.migration.provider=singleFile -Dkeycloak.migration.realmName=$1 -Dkeycloak.migration.file=/opt/jboss/keycloak/keycloak-export.json -Djboss.http.port=8888 -Djboss.https.port=9999 -Djboss.management.http.port=7777"
docker cp $2:/opt/jboss/keycloak/keycloak-export.json .
