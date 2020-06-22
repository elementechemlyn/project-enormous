"""
An example of the testviewer client from lhcr1 authenticating a user and then
exchanging the users token for a toke minted at lhcr2
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

def exchange_token( oidc_obj, token, subject_issuer):
    """
    """
    params_path = {"realm-name": oidc_obj.realm_name}
    payload = {"client_id": oidc_obj.client_id, 
            "grant_type": 'urn:ietf:params:oauth:grant-type:token-exchange',
            "subject_token":token,
            "subject_issuer":subject_issuer}

    payload = oidc_obj._add_secret_key(payload)
    data_raw = oidc_obj.connection.raw_post(URL_TOKEN.format(**params_path),
                                        data=payload)
    return raise_error_from_response(data_raw, KeycloakGetError)


LHCR1_SERVER_URL = "http://192.168.0.36:8081/auth/"
LHCR1_REALM_NAME = "lhcr1"
LHCR1_CLIENT_ID = "testviewer"
LHCR1_CLIENT_SECRET = "85ac8b3e-df3c-4e4f-be65-ca5e5b68d3dc"

LHCR2_SERVER_URL = "http://192.168.0.36:8082/auth/"
LHCR2_REALM_NAME = "lhcr2"
LHCR2_CLIENT_ID = "lhcr1_testviewer"
LHCR2_CLIENT_SECRET = "91568b49-bb6d-4197-90f7-132e9db5fe16"


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

lhcr2token = exchange_token(lhcr2oidc,lhcr1token['access_token'],"lhcr1oidc")
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

