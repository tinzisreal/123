from flask_appbuilder.security.manager import AUTH_OAUTH
from superset.security import SupersetSecurityManager
import logging

SECRET_KEY = 'tungdeptrai'

# Enable OAuth authentication
AUTH_TYPE = AUTH_OAUTH
LOGOUT_REDIRECT_URL = 'http://localhost:8180/realms/jmix-realm/protocol/openid-connect/logout'
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = 'Gamma'

HTTP_HEADERS = {
    "X-Frame-Options": "ALLOWALL"
}
OAUTH_PROVIDERS = [
    {
        "name": "keycloak",   # tên provider, sẽ hiển thị nút "Login with kc"
        "icon": "fa-key",
        "token_key": "access_token",
        "remote_app": {
            "client_id": "superset",
            "client_secret": "aV6762iYNwmXaqqPb4tFuhrXkqEQ17Il",
            "server_metadata_url": "http://keycloak.local:8180/realms/jmix-realm/.well-known/openid-configuration",
            "client_kwargs": {"scope": "openid profile email"},
        },
    }
]

LOG_LEVEL = "DEBUG"
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("flask_oauthlib").setLevel(logging.DEBUG)
logging.getLogger("authlib").setLevel(logging.DEBUG)
logging.getLogger("superset.security").setLevel(logging.DEBUG)
logging.getLogger("flask_appbuilder.security").setLevel(logging.DEBUG)

log = logging.getLogger(__name__)

class KeycloakSecurity(SupersetSecurityManager):
    """
    Custom SecurityManager để lấy user info từ Keycloak
    """

    def oauth_user_info(self, provider, resp=None):
        if provider == "keycloak":
            log.debug("Keycloak response received: %s", resp)
            # Gọi trực tiếp endpoint userinfo
            me = self.appbuilder.sm.oauth_remotes[provider].get(
                "http://keycloak.local:8180/realms/jmix-realm/protocol/openid-connect/userinfo"
            )
            me.raise_for_status()
            data = me.json()
            log.debug("User info from Keycloak: %s", data)

            return {
                "username": data.get("preferred_username"),
                "first_name": data.get("given_name", ""),
                "last_name": data.get("family_name", ""),
                "email": data.get("email", ""),
                "role_keys": data.get("roles", []),
            }

CUSTOM_SECURITY_MANAGER = KeycloakSecurity

GUEST_ROLE_NAME = 'Gamma'
FEATURE_FLAGS = {
    "EMBEDDED_SUPERSET": True,
}
TALISMAN_CONFIG = {
    "content_security_policy": {
        "base-uri": ["'self'"],
        "default-src": ["'self'"],
        "img-src": [
            "'self'",
            "blob:",
            "data:",
            "https://apachesuperset.gateway.scarf.sh",
            "https://static.scarf.sh/",
        ],
        "worker-src": ["'self'", "blob:"],
        "connect-src": [
            "'self'",
            "https://api.mapbox.com",
            "https://events.mapbox.com",
        ],
        "object-src": "'none'",
        "style-src": [
            "'self'",
            "'unsafe-inline'",
        ],
        "script-src": ["'self'", "'strict-dynamic'"],
        "frame-ancestors": ["http://localhost:8080"]
    },
    "content_security_policy_nonce_in": ["script-src"],
    "force_https": False,
    "session_cookie_secure": False,

}
