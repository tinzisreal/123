# """
# Superset Configuration for Docker with Keycloak OAuth Integration
# """
# import logging
# from flask import request, session
# from flask_appbuilder.security.manager import AUTH_OAUTH
# from superset.security import SupersetSecurityManager
# from flask import Response

# # =============================================================================
# # BASIC CONFIGURATION
# # =============================================================================
# SECRET_KEY = "123123123"

# # =============================================================================
# # AUTHENTICATION CONFIGURATION
# # =============================================================================
# AUTH_TYPE = AUTH_OAUTH
# AUTH_USER_REGISTRATION = True
# AUTH_USER_REGISTRATION_ROLE = "Gamma"
# AUTH_ROLE_ADMIN = "Admin"
# AUTH_ROLES_SYNC_AT_LOGIN = True

# # =============================================================================
# # OAUTH PROVIDERS CONFIGURATION
# # =============================================================================
# OAUTH_PROVIDERS = [
#     {
#         "name": "keycloak",
#         "icon": "fa-key",
#         "token_key": "access_token",
#         "remote_app": {
#             "client_id": "superman",
#             "client_secret": "iadJ87dba8b32TfnymdBpVxpLcYsheWL",
#             "server_metadata_url": "http://keycloak.local:8180/realms/master/.well-known/openid-configuration",
#             "client_kwargs": {"scope": "openid profile email"},
#         },
#     }
# ]

# # =============================================================================
# # LOGGING CONFIGURATION
# # =============================================================================
# LOG_LEVEL = "DEBUG"
# logging.basicConfig(level=logging.DEBUG)
# logging.getLogger("flask_oauthlib").setLevel(logging.DEBUG)
# logging.getLogger("authlib").setLevel(logging.DEBUG)
# logging.getLogger("superset.security").setLevel(logging.DEBUG)
# logging.getLogger("flask_appbuilder.security").setLevel(logging.DEBUG)

# logger = logging.getLogger(__name__)

# # =============================================================================
# # CUSTOM SECURITY MANAGER
# # =============================================================================
# class KeycloakSecurityManager(SupersetSecurityManager):
#     """Custom Security Manager for Keycloak OAuth integration"""

#     def oauth_user_info(self, provider, resp=None):
#         """Lấy thông tin user + lưu id_token vào session"""
#         if provider == "keycloak":
#             logger.debug("Keycloak response received: %s", resp)
#             try:
#                 # Lưu id_token lại để dùng cho logout
#                 if resp and "id_token" in resp:
#                     session["id_token"] = resp["id_token"]
#                     logger.debug("Saved id_token into session")

#                 me = self.appbuilder.sm.oauth_remotes[provider].get(
#                     "http://keycloak.local:8180/realms/master/protocol/openid-connect/userinfo"
#                 )
#                 me.raise_for_status()
#                 data = me.json()
#                 logger.debug("User info from Keycloak: %s", data)
#                 return {
#                     "username": data.get("preferred_username"),
#                     "first_name": data.get("given_name", ""),
#                     "last_name": data.get("family_name", ""),
#                     "email": data.get("email", ""),
#                     "role_keys": data.get("roles", []),
#                 }
#             except Exception as e:
#                 logger.error("Error getting user info from Keycloak: %s", e)
#                 return None

#     def logout(self):
#         """Logout Superset + Keycloak (silent redirect)"""
#         logger.debug("🚪 Superset logout triggered")
#         super().logout()  # clear Superset session

#         base_url = "http://keycloak.local:8180/realms/master/protocol/openid-connect/logout"
#         redirect_uri = "http://localhost:8088/login/"
#         id_token = session.get("id_token")

#         if id_token:
#             logout_url = f"{base_url}?id_token_hint={id_token}&post_logout_redirect_uri={redirect_uri}"
#         else:
#             logout_url = f"{base_url}?client_id=superman&post_logout_redirect_uri={redirect_uri}"

#         logger.debug("🔗 Redirecting to Keycloak logout: %s", logout_url)
#         return redirect(logout_url)


# CUSTOM_SECURITY_MANAGER = KeycloakSecurityManager
# AUTH_ROLES_MAPPING = {
#     "superset_users": ["Gamma", "Alpha"],
#     "KeycloakAdmin": ["Admin"],
#     "admin": ["Admin"],   # thêm dòng này
# }
# # =============================================================================
# # APPLICATION CONFIGURATION
# # =============================================================================
# GUEST_ROLE_NAME = "Gamma"
# FEATURE_FLAGS = {"EMBEDDED_SUPERSET": True}

# HTTP_HEADERS = {"X-Frame-Options": "ALLOWALL"}


# TALISMAN_CONFIG = {
#     "content_security_policy": {
#         "default-src": ["'self'"],
#         "img-src": ["'self'", "blob:", "data:"],
#         "style-src": ["'self'", "'unsafe-inline'"],
#         "script-src": ["'self'", "'unsafe-inline'"],
#         "frame-ancestors": ["http://localhost:8080"],
#     },
#     "force_https": False,
#     "session_cookie_secure": False,
# }

# # =============================================================================
# # CUSTOM FLASK APP MUTATOR
# # =============================================================================
# def FLASK_APP_MUTATOR(app):
#     from flask import Blueprint, jsonify

#     # inject script vào welcome page
#     @app.after_request
#     def handle_popup_behavior(response):
#         if response.mimetype == "text/html":
#             body = response.get_data(as_text=True)
#             if request.path.startswith("/superset/welcome"):
#                 body = _inject_login_success_script(body)
#                 response.set_data(body)
#         return response

#     # route callback khi Keycloak logout xong
#     bp = Blueprint("custom_logout", __name__)


#     @bp.route("/api/clear-superset-session")
#     def clear_superset_session():
#         try:
#             session.clear()
#             logger.debug("✅ Superset session cleared")
#             return jsonify({"status": "ok"})
#         except Exception as e:
#             logger.error("❌ Error clearing session: %s", e)
#             return jsonify({"status": "error", "msg": str(e)}), 500


#     @bp.route("/api/get-logout-url")
#     def get_logout_url():
#         base_url = "http://keycloak.local:8180/realms/master/protocol/openid-connect/logout"
#         kc_callback = "http://localhost:8088/keycloak-logout-success"

#         id_token = session.get("id_token")
#         if id_token:
#             logout_url = f"{base_url}?id_token_hint={id_token}&post_logout_redirect_uri={kc_callback}"
#         else:
#             logout_url = f"{base_url}?client_id=superman&post_logout_redirect_uri={kc_callback}"

#         return jsonify({"logout_url": logout_url})

#     # --- callback sau khi Keycloak logout ---
#     @bp.route("/keycloak-logout-success")
#     def keycloak_logout_success():
#         session.clear()  # 👉 Clear Superset session sau khi Keycloak logout xong
#         return """
#         <script>
#           console.log("✅ Keycloak logout success page loaded");
#           if (window.opener) {
#             window.opener.postMessage("kc-logout-success", "*");
#             window.close();
#           }
#         </script>
#         """

#     app.register_blueprint(bp)
#     return app


# def _inject_login_success_script(body):
#     script = """
#     <script>
#         (function() {
#             if (window.opener && !window.opener.closed) {
#                 window.opener.location.reload();
#                 window.open('', '_self');
#                 window.close();
#             }
#         })();
#     </script>
#     """
#     return body.replace("</body>", script + "</body>")
"""
Superset Configuration for Docker with Keycloak OAuth Integration
"""
import logging
from flask import request, session, redirect
from flask_appbuilder.security.manager import AUTH_OAUTH, AUTH_DB
from superset.security import SupersetSecurityManager
import os

# =============================================================================
# BASIC CONFIGURATION
# =============================================================================
SECRET_KEY = "123123123"
SQLALCHEMY_DATABASE_URI = os.environ.get(
    "SQLALCHEMY_DATABASE_URI",
    "postgresql+psycopg2://superset:superset@db:5432/superset"
)
AUTH_TYPE = AUTH_OAUTH
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Gamma"
AUTH_ROLE_ADMIN = "Admin"
AUTH_ROLES_SYNC_AT_LOGIN = True
SHOW_STACKTRACE = True
AUTH_DB = True          # 👈 Cho phép login bằng username/password qua API
WTF_CSRF_ENABLED = False

OAUTH_PROVIDERS = [
    {
        "name": "keycloak",
        "icon": "fa-key",
        "token_key": "access_token",
        "remote_app": {
            "client_id": "superman",
            "client_secret": "iadJ87dba8b32TfnymdBpVxpLcYsheWL",
            "server_metadata_url": "http://keycloak.local:8180/realms/master/.well-known/openid-configuration",
            "client_kwargs": {"scope": "openid profile email"},
        },
    }
]

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logging.getLogger("superset").setLevel(logging.DEBUG)
logging.getLogger("flask_appbuilder").setLevel(logging.DEBUG)
logging.getLogger("authlib").setLevel(logging.DEBUG)

# =============================================================================
# CUSTOM SECURITY MANAGER
# =============================================================================
class KeycloakSecurityManager(SupersetSecurityManager):
    def oauth_user_info(self, provider, resp=None):
        if provider == "keycloak":
            logger.debug("Keycloak response received: %s", resp)
            try:
                if resp and "id_token" in resp:
                    session["id_token"] = resp["id_token"]
                    logger.debug("💾 Saved id_token into session")

                me = self.appbuilder.sm.oauth_remotes[provider].get(
                    "http://keycloak.local:8180/realms/master/protocol/openid-connect/userinfo"
                )
                me.raise_for_status()
                data = me.json()
                logger.debug("User info from Keycloak: %s", data)
                return {
                    "username": data.get("preferred_username"),
                    "first_name": data.get("given_name", ""),
                    "last_name": data.get("family_name", ""),
                    "email": data.get("email", ""),
                    "role_keys": data.get("roles", []),
                }
            except Exception as e:
                logger.error("Error getting user info from Keycloak: %s", e)
                return None


CUSTOM_SECURITY_MANAGER = KeycloakSecurityManager

AUTH_ROLES_MAPPING = {
    "superset_users": ["Gamma", "Alpha"],
    "KeycloakAdmin": ["Admin"],
    "admin": ["Admin"],
}

# =============================================================================
# APPLICATION CONFIGURATION
# =============================================================================
GUEST_ROLE_NAME = "Gamma"
FEATURE_FLAGS = {"EMBEDDED_SUPERSET": True}
HTTP_HEADERS = {"X-Frame-Options": "ALLOWALL"}
SESSION_COOKIE_SAMESITE = None
TALISMAN_CONFIG = {
    "content_security_policy": {
        "default-src": ["'self'"],
        "img-src": ["'self'", "blob:", "data:"],
        "style-src": ["'self'", "'unsafe-inline'"],
        "script-src": ["'self'", "'unsafe-inline'"],
        "frame-ancestors": ["http://localhost:8080"],
    },
    "force_https": False,
    "session_cookie_secure": False,
}

# =============================================================================
# CUSTOM FLASK APP MUTATOR
# =============================================================================
def FLASK_APP_MUTATOR(app):
    from flask import Blueprint, request, session, redirect

    bp = Blueprint("custom_logout", __name__)

    @bp.route("/logout/keycloak")
    def custom_logout():
        """Clear Superset session + logout Keycloak"""
        logger.debug("🚪 Custom Superset+Keycloak logout triggered")
        id_token = session.get("id_token")
        session.clear()

        base_url = "http://keycloak.local:8180/realms/master/protocol/openid-connect/logout"
        redirect_uri = "http://localhost:8088/login/"

        if id_token:
            logout_url = f"{base_url}?id_token_hint={id_token}&post_logout_redirect_uri={redirect_uri}"
        else:
            logout_url = f"{base_url}?client_id=superman&post_logout_redirect_uri={redirect_uri}"

        logger.debug("🔗 Redirecting to Keycloak logout: %s", logout_url)
        return redirect(logout_url)

    app.register_blueprint(bp)

    @app.after_request
    def inject_custom_scripts(response):
        try:
            if response.mimetype == "text/html":  # inject mọi HTML response, kể cả login
                body = response.get_data(as_text=True)
                if "</body>" in body:
                    logger.debug("💉 Injecting custom script vào %s", request.path)
                    body = body.replace(
                        "</body>",
                        """
                        <script>
                            console.log("✅ Injected custom login/logout script");
                            if (window.opener && !window.opener.closed) {
                                console.log("🔄 Reload opener after login success");
                                window.opener.location.reload();
                                window.open('', '_self');
                                window.close();
                            }
                            const observer = new MutationObserver(() => {
                                const logoutLink = document.querySelector("a[href='/logout/']");
                                if (logoutLink) {
                                    console.log("🎯 Found logout link, đổi sang /logout/keycloak");
                                    logoutLink.setAttribute("href", "/logout/keycloak");
                                    logoutLink.textContent = "Logout Full";
                                    observer.disconnect();
                                }
                            });
                            observer.observe(document.body, { childList: true, subtree: true });
                        </script>
                        </body>
                        """,
                    )
                    response.set_data(body)
        except Exception as e:
            logger.error("⚠️ Lỗi khi inject script: %s", e)

        return response

    return app



# =============================================================================
# THEME CUSTOMIZATION
# =============================================================================




APP_ICON = "/static/assets/images/quandoi.png"
LOGO_TARGET_PATH = '/superset/welcome'
LOGO_TOOLTIP = 'Welcome to Quanluc Dashboard'
LOGO_RIGHT_TEXT = "Quản lý quân lực"
APP_NAME = "Quản lý quân lực"
