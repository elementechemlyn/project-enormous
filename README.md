## Network Details 

## LHCR one

| Service | Docker Host | Docker Port | Host Port|
|---------|-------------|-------------|-----------|
| Keycloak Backend | lhcr1-keycloak | 8080 | N/A|
| Keycloak Frontend | lhcr1-keycloak | 8081 | 8081|  
| Kong API Endpoints | lhcr1-kong | 8000 | 8000 | 
| Kong Secure API Endpoints | lhcr1-kong | 8443 | 8443 |
| Kong Admin | lhcr1-kong | 8001 | 8001|
| Kong Secure Admin | lhcr1-kong | 8444 | 8444 |
| Postgres   | lhcr1-kong-db | 5432 | 6431|
| FHIR Server| lhcr1-fhirserver | 8080 | N/A** |
| FHIR Viewer | lhcr1-viewer | 9090 | N/A** |

** Service accesed via Kong

### LHCR two

| Service | Docker Host | Docker Port | Host Port|
|---------|-------------|-------------|-----------|
| Keycloak Backend | lhcr2-keycloak | 8080 | N/A| 
| Keycloak Frontend | lhcr2-keycloak | 8081 | 8082| 
| Kong API Endpoints | lhcr2-kong | 8000 | 8002|
| Kong Secure API Endpoints | lhcr2-kong | 8443 | 8445|
| Kong Admin | lhcr2-kong | 8001 | 8004 |
| Kong Secure Admin | lhcr2-kong | 8444 | 8446 |
| Postgres   | lhcr2-kong-db | 5432 | 6432 |
| FHIR Server| lhcr2-fhirserver | 8080 | N/A** |
| FHIR Viewer | lhcr2-viewer | 9090 | N/A** |

** Service accesed via Kong

## Kong Proxy Paths
| Service | Path |
|-----|-----|
| FHIR Server | /fhir |
| FHIR Test UI| /viewer |

## Keycloak users

### Lhcr1

| User | Password | Role | Smart Scope
|------|----------|-----|----
| user1| user1    | clinical | \*.*

### Lhcr2

| User | Password | Role| Smart Scope
|------|----------|-----|-----
| user2| user2    | clinical | \*.*

## Keycloak Clients

### Lhcr1

b2c55a04-3ac4-4545-bb0c-da063b9e4a9e

| ClientID | Client Secret | Use
|------|----------|-----
| kong| 0efb256c-cdb9-439b-9767-c6b997a4e827 | Used by API gateway to authenticate requests
| testviewer| 85ac8b3e-df3c-4e4f-be65-ca5e5b68d3dc | Used by the FHIR Test Viewer to authenticate user
| lhcr2_keycloak| fdfb428e-6415-4073-8bc8-32a1a2061067 | Used by the LHCR2 Keycloak to access Userinfo endpoint
| lhcr2_testviewer| a4d8acc4-48ba-46fe-a46a-99a7bf6bb8fe | Used by the LHCR2 FHIR Test Viewer to exchange a token

### Lhcr2
| ClientID | Client Secret | Use
|------|----------|-----
| kong| b2c55a04-3ac4-4545-bb0c-da063b9e4a9e| Used by API gateway to authenticate requests
| testviewer| 5244c131-ae37-4b37-a015-c4d1e587034a | Used by the FHIR Test Viewer to authenticate user
| lhcr1_keycloak| 7193c27b-e93c-459a-91b7-fc91abb464a2 | Used by the LHCR1 Keycloak to access Userinfo endpoint
| lhcr1_testviewer| 91568b49-bb6d-4197-90f7-132e9db5fe16 | Used by the LHCR1 FHIR Test Viewer to exchange a token

## Export the Keycloak config

bin/standalone.sh -Dkeycloak.migration.usersExportStrategy=SAME_FILE -Dkeycloak.migration.action=export -Dkeycloak.migration.provider=singleFile -Dkeycloak.migration.realmName=lhcr1 -Dkeycloak.migration.file=keycloak-export.json -Djboss.http.port=8888 -Djboss.https.port=9999 -Djboss.management.http.port=7777