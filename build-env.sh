#!/bin/bash
. .env
. _network_functions

(set -e
  if [[ -z "$IP" ]]; then
    echo "Please set the IP var to your local IP address. Example: export IP=192.168.0.1"
    exit 1
  fi

  (set -x
    # (TODO - set up the docker networks properly i.e. use add-hosts and don't assume everything is on the same host)
    # Tear down environment if it is running
    docker-compose -f docker-compose.lhcr1.yml down
    docker-compose -f docker-compose.lhcr2.yml down
    docker build --build-arg KONG_BASE_TAG=${KONG_BASE_TAG} -t lhcr/kong-oidc .
    docker-compose -f docker-compose.lhcr2.yml up -d lhcr2_kong-db
    docker-compose -f docker-compose.lhcr1.yml up -d lhcr1_kong-db
  )
  _wait_for_listener localhost:${LHCR2_KONG_DB_PORT}
  _wait_for_listener localhost:${LHCR1_KONG_DB_PORT}

  (set -x
    docker-compose -f docker-compose.lhcr2.yml run --rm lhcr2_kong kong migrations bootstrap
    docker-compose -f docker-compose.lhcr2.yml run --rm lhcr2_kong kong config db_import /tmp/kong.yml
    docker-compose -f docker-compose.lhcr1.yml run --rm lhcr1_kong kong migrations bootstrap
    docker-compose -f docker-compose.lhcr1.yml run --rm lhcr1_kong kong config db_import /tmp/kong.yml
    docker-compose -f docker-compose.lhcr1.yml up -d
    docker-compose -f docker-compose.lhcr2.yml up -d
  )

)