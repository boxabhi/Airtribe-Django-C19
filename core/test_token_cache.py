import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django

django.setup()

from django.core.cache import cache
from django.conf import settings
from django.db import connection
from django.test import Client
from django.test.utils import CaptureQueriesContext
from rest_framework.authtoken.models import Token

from home.middleware import get_token_user_cache_key


def print_queries(label, queries):
    print(f'\n{label}')
    print(f'Total SQL queries: {len(queries)}')
    for index, query in enumerate(queries, start=1):
        print(f'  Query {index}: {query["sql"]}')


def run_request(client, token, request_number):
    cache_key = get_token_user_cache_key(token)
    cached_before = cache.get(cache_key)
    cache_status = 'HIT' if cached_before is not None else 'MISS'

    print(f'\n--- Request {request_number} ---')
    print(f'Cache key: {cache_key}')
    print(f'Cache status before request: {cache_status}')
    print(f'Cache before request: {cached_before!r}')

    with CaptureQueriesContext(connection) as captured:
        response = client.get('/api/dashboard/', HTTP_AUTHORIZATION=f'Token {token}')

    cached_after = cache.get(cache_key)
    print(f'Status code: {response.status_code}')
    print(f'Response JSON: {response.json()}')
    print(f'Cache after request: {cached_after!r}')
    print_queries('SQL executed', captured.captured_queries)


def main():
    if 'testserver' not in settings.ALLOWED_HOSTS:
        settings.ALLOWED_HOSTS.append('testserver')

    token = sys.argv[1] if len(sys.argv) > 1 else None
    if token is None:
        token_record = Token.objects.select_related('user').first()
        if token_record is None:
            print('No token found.')
            print('Create users first:')
            print('  python manage.py seed_token_users --count 5 --password test-password')
            sys.exit(1)
        token = token_record.key
        print(f'Using first token from DB for user: {token_record.user.username}')

    cache_key = get_token_user_cache_key(token)
    cache.delete(cache_key)
    print(f'Deleted existing cache value for: {cache_key}')

    client = Client()
    run_request(client, token, 1)
    run_request(client, token, 2)


if __name__ == '__main__':
    main()
