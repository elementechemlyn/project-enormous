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

def exchange_token( oidc_obj, token):
    """
    """
    params_path = {"realm-name": oidc_obj.realm_name}
    payload = {"client_id": oidc_obj.client_id, 
            "grant_type": 'urn:ietf:params:oauth:grant-type:token-exchange',
            "subject_token":token,
            "subject_issuer":"lhcr2oidc"}

    payload = oidc_obj._add_secret_key(payload)
    data_raw = oidc_obj.connection.raw_post(URL_TOKEN.format(**params_path),
                                        data=payload)
    return raise_error_from_response(data_raw, KeycloakGetError)


SERVER_URL = "http://192.168.0.36:8082/auth/"
REALM_NAME = "lhcr2"
CLIENT_ID = "pyflask"
CLIENT_SECRET = "5244c131-ae37-4b37-a015-c4d1e587034a"
#Get a token from lhcr2
lhcr2oidc = KeycloakOpenID(server_url=SERVER_URL,
                          client_id=CLIENT_ID,
                          realm_name=REALM_NAME,
                          client_secret_key=CLIENT_SECRET,
                          verify=True)

lhcr2token = lhcr2oidc.token("user2","user2")
print(lhcr2token)
#Exchange it for a token from lhcr1
SERVER2_URL = "http://192.168.0.36:8081/auth/"
REALM2_NAME = "lhcr1"
CLIENT2_ID = "pyflask_lhcr2"
CLIENT2_SECRET = "a4d8acc4-48ba-46fe-a46a-99a7bf6bb8fe"

lhcr1oidc = KeycloakOpenID(server_url=SERVER2_URL,
                          client_id=CLIENT2_ID,
                          realm_name=REALM2_NAME,
                          client_secret_key=CLIENT2_SECRET,
                          verify=True)
lhcr1token = exchange_token(lhcr1oidc,lhcr2token['access_token'])
print(lhcr1token)
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

