#!/bin/bash
. .env
. _network_functions

(set -e
  (set -x
    # (TODO - set up the docker networks properly! i.e. use add-hosts and don't assume everything is on the same host!)
    # Tear down environment if it is running
    docker-compose -f docker-compose.lhcr1.yml down
    docker-compose -f docker-compose.lhcr2.yml down
  )
)