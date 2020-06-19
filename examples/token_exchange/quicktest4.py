"""
bin/standalone.sh -Dkeycloak.migration.action=export -Dkeycloak.migration.provider=singleFile -Dkeycloak.migration.file=keycloak-export.json -Djboss.http.port=8888 -Djboss.https.port=9999 -Djboss.management.http.port=7777

docker run -p 8082:8080 -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=admin -e KEYCLOAK_IMPORT=/tmp/lhcr1.json -v "$(pwd)"/lhcr2-keycloak-export.json:/tmp/lhcr1.json jboss/keycloak -Dkeycloak.profile.feature.token_exchange=enabled -Dkeycloak.profile.feature.admin_fine_grained_authz=enabled

"""
from keycloak import KeycloakAdmin, KeycloakOpenID
from keycloak.exceptions import raise_error_from_response, KeycloakGetError
from keycloak.urls_patterns import (
    URL_AUTH,
    URL_TOKEN,
    URL_USERINFO,
    URL_WELL_KNOWN,
    URL_LOGOUT,
    URL_CERTS,
    URL_ENTITLEMENT,
    URL_INTROSPECT
)
import requests

def exchange_token( oidc_obj, token, subject_issuer, client_secret):
    params_path = {"realm-name": oidc_obj.realm_name}
    payload = {"client_id": oidc_obj.client_id, 
            "client_secret" : client_secret,
            "grant_type": 'urn:ietf:params:oauth:grant-type:token-exchange',
            "subject_token":token,
            "subject_issuer":subject_issuer}

    url_path  = 'realms/%(realm-name)s/protocol/openid-connect/token' % (params_path)
    url = oidc_obj._connection._base_url + url_path
    response = requests.post(url,data=payload)
    return response.json()

LHCR1_SERVER_URL = "http://192.168.0.36:8081/auth/"
LHCR1_REALM_NAME = "lhcr1"
LHCR1_CLIENT_ID = "pyflask_lhcr2"
LHCR1_CLIENT_SECRET = "a4d8acc4-48ba-46fe-a46a-99a7bf6bb8fe"

LHCR2_SERVER_URL = "http://192.168.0.36:8082/auth/"
LHCR2_REALM_NAME = "lhcr2"
LHCR2_CLIENT_ID = "pyflask"
LHCR2_CLIENT_SECRET = "5244c131-ae37-4b37-a015-c4d1e587034a"


#Get a token from lhcr1
lhcr1oidc = KeycloakOpenID(server_url=LHCR1_SERVER_URL,
                          client_id=LHCR1_CLIENT_ID,
                          realm_name=LHCR1_REALM_NAME,
                          client_secret_key=LHCR1_CLIENT_SECRET,
                          verify=True)

lhcr1token = lhcr1oidc.token("user1","user1")

print(lhcr1token)

#Exchange it for a token from lhcr2
lhcr2oidc = KeycloakOpenID(server_url=LHCR2_SERVER_URL,
                          client_id=LHCR2_CLIENT_ID,
                          realm_name=LHCR2_REALM_NAME,
                          client_secret_key=LHCR2_CLIENT_SECRET,
                          verify=True)

lhcr2token = exchange_token(lhcr2oidc,lhcr1token['access_token'],"lhcr1oidc", LHCR2_CLIENT_SECRET)
print(lhcr2token)

"""
curl -X POST \
    -d "client_id=starting-client" \
    -d "client_secret=geheim" \
    --data-urlencode "grant_type=urn:ietf:params:oauth:grant-type:token-exchange" \
    -d "subject_token=...." \
    -d "subject_issuer=myOidcProvider" \
    --data-urlencode "subject_token_type=urn:ietf:params:oauth:token-type:access_token" \
    -d "audience=target-client" \
    http://localhost:8080/auth/realms/myrealm/protocol/openid-connect/token
"""

