from django.contrib.auth.models import AnonymousUser, User
from django.core.cache import cache
from django.test import RequestFactory, TestCase, override_settings
from rest_framework.authtoken.models import Token

from home.middleware import CachedTokenAuthenticationMiddleware

# Create your tests here.


@override_settings(CACHES={
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'test-token-auth-cache',
    }
})
class CachedTokenAuthenticationMiddlewareTests(TestCase):
    def setUp(self):
        cache.clear()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='alice',
            password='secret-password',
        )
        self.token, _ = Token.objects.get_or_create(user=self.user)

    def test_token_authentication_caches_user_id(self):
        middleware = CachedTokenAuthenticationMiddleware(lambda request: request)
        request = self.factory.get(
            '/',
            HTTP_AUTHORIZATION=f'Token {self.token.key}',
        )

        with self.assertNumQueries(1):
            middleware(request)

        self.assertEqual(request.user, self.user)
        self.assertEqual(request.token_auth_cache_status, 'MISS')
        self.assertEqual(request.token_auth_user_source, 'DATABASE_TOKEN_LOOKUP')

        cached_request = self.factory.get(
            '/',
            HTTP_AUTHORIZATION=f'Token {self.token.key}',
        )

        with self.assertNumQueries(1):
            middleware(cached_request)

        self.assertEqual(cached_request.user, self.user)
        self.assertEqual(cached_request.token_auth_cache_status, 'HIT')
        self.assertEqual(cached_request.token_auth_user_source, 'REDIS_CACHE_USER_ID')

    def test_invalid_token_is_cached(self):
        middleware = CachedTokenAuthenticationMiddleware(lambda request: request)
        request = self.factory.get('/', HTTP_AUTHORIZATION='Token bad-token')

        with self.assertNumQueries(1):
            middleware(request)

        self.assertIsInstance(request.user, AnonymousUser)
        self.assertEqual(request.token_auth_cache_status, 'MISS')
        self.assertEqual(request.token_auth_user_source, 'INVALID_TOKEN')

        cached_request = self.factory.get('/', HTTP_AUTHORIZATION='Token bad-token')

        with self.assertNumQueries(0):
            middleware(cached_request)

        self.assertIsInstance(cached_request.user, AnonymousUser)
        self.assertEqual(cached_request.token_auth_cache_status, 'HIT')
        self.assertEqual(cached_request.token_auth_user_source, 'INVALID_TOKEN_CACHE')
