import hashlib

from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.core.cache import cache
from rest_framework.authtoken.models import Token


INVALID_USER_ID = 0


def get_token_user_cache_key(token):
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    return f'token_auth:user_id:{token_hash}'


class CachedTokenAuthenticationMiddleware:
    """
    Authenticates requests with Authorization: Token <key> or Bearer <key>.

    The middleware caches token -> user_id, so repeated token-authenticated
    requests do not need to query the token table before loading the user.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.cache_timeout = getattr(settings, 'TOKEN_AUTH_CACHE_TIMEOUT', 300)

    def __call__(self, request):
        request.token_auth_cache_key = None
        request.token_auth_cache_status = 'NO_TOKEN'
        request.token_auth_user_source = 'NO_TOKEN'

        token = self._get_token(request)
        if token:
            self._authenticate(request, token)
        return self.get_response(request)

    def _authenticate(self, request, token):
        cache_key = get_token_user_cache_key(token)
        request.token_auth_cache_key = cache_key
        user_id = cache.get(cache_key)

        if user_id is None:
            request.token_auth_cache_status = 'MISS'
            token_record = (
                Token.objects
                .select_related('user')
                .filter(key=token)
                .first()
            )
            if token_record is None:
                cache.set(cache_key, INVALID_USER_ID, self.cache_timeout)
                request.token_auth_user_source = 'INVALID_TOKEN'
                request.user = AnonymousUser()
                return

            user_id = token_record.user_id
            cache.set(cache_key, user_id, self.cache_timeout)
            request.token_auth_user_source = 'DATABASE_TOKEN_LOOKUP'
            request.user = token_record.user
            return

        request.token_auth_cache_status = 'HIT'

        if user_id == INVALID_USER_ID:
            request.token_auth_user_source = 'INVALID_TOKEN_CACHE'
            request.user = AnonymousUser()
            return

        try:
            request.user = User.objects.get(pk=user_id, is_active=True)
            request.token_auth_user_source = 'REDIS_CACHE_USER_ID'
        except User.DoesNotExist:
            cache.delete(cache_key)
            request.token_auth_user_source = 'STALE_CACHE_DELETED'
            request.user = AnonymousUser()

    def _get_token(self, request):
        header = request.META.get('HTTP_AUTHORIZATION', '')
        if not header:
            return None

        parts = header.split()
        if len(parts) != 2:
            return None

        keyword, token = parts
        if keyword.lower() not in {'token', 'bearer'}:
            return None
        return token

    def _cache_key(self, token):
        return get_token_user_cache_key(token)
