from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")


class CookieJWTAuthentication(JWTAuthentication):
    """
    Tries Authorization header first (standard SimpleJWT behavior),
    then falls back to reading the access token from a cookie.
    Enforces CSRF protection when authenticating via cookie on unsafe methods.
    """

    # Set your cookie names here if you like
    access_cookie_name = "accessToken"  # e.g. 'access' or 'access_token'

    def authenticate(self, request):
        # 1) Try standard header-based auth
        header = self.get_header(request)
        if header is not None:
            raw_token = self.get_raw_token(header)
            if raw_token is not None:
                validated = self.get_validated_token(raw_token)
                return self.get_user(validated), validated

        # 2) Fallback to cookie-based auth
        raw_token = request.COOKIES.get(self.access_cookie_name)
        if not raw_token:
            return None  # No auth

        # CSRF required when using cookie-based auth for unsafe methods
        if request.method not in SAFE_METHODS:
            self._enforce_csrf(request)

        validated = self.get_validated_token(raw_token)
        return self.get_user(validated), validated

    def _enforce_csrf(self, request):
        """
        Raise AuthenticationFailed if CSRF check fails.
        Expect the 'X-CSRFToken' header to match the 'csrftoken' cookie.
        """
        reason = CsrfViewMiddleware(lambda r: None).process_view(request, None, (), {})
        if reason:
            raise exceptions.AuthenticationFailed(f"CSRF Failed: {reason}")
