## Network Details 

## LHCR one

| Service | Docker Host | Docker Port | Local Port|
|---------|-------------|-------------|-----------|
| Keycloak Backend | lhcr1_keycloak | 8080 | N/A|
| Keycloak Frontend | lhcr1_keycloak | 8081 | 8081|  
| Kong API Endpoints | lhcr1_kong | 8000 | 8000 | 
| Kong Secure API Endpoints | lhcr1_kong | 8443 | 8443 |
| Kong Admin | lhcr1_kong | 8001 | 8001|
| Kong Secure Admin | lhcr1_kong | 8444 | 8444 |
| Postgres   | lhcr1_kong-db | 5432 | 6431|
| FHIR Server| lhcr1_fhirserver | 8080 | N/A |
| FHIR Viewer | lhcr1_viewer | 9090 | N/A |

### LHCR two

| Service | Docker Host | Docker Port | Local Port|
|---------|-------------|-------------|-----------|
| Keycloak Backend | lhcr2_keycloak | 8080 | N/A| 
| Keycloak Frontend | lhcr2_keycloak | 8081 | 8082| 
| Kong API Endpoints | lhcr2_kong | 8000 | 8002|
| Kong Secure API Endpoints | lhcr1_kong | 8443 | 8445|
| Kong Admin | lhcr2_kong | 8001 | 8004 |
| Kong Secure Admin | lhcr1_kong | 8444 | 8446 |
| Postgres   | lhcr2_kong-db | 5432 | 6432 |
| FHIR Server| lhcr2_fhirserver | 8080 | N/A |
| FHIR Viewer | lhcr2_viewer | 9090 | N/A |

## Kong/Proxy Paths

| FHIR Server | /fhir |
| FHIR Test UI| /viewer |
