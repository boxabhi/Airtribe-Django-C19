from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = 'Create multiple users with the same password and auth tokens.'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10)
        parser.add_argument('--password', default='test-password')
        parser.add_argument('--prefix', default='token_user')

    @transaction.atomic
    def handle(self, *args, **options):
        count = options['count']
        password = options['password']
        prefix = options['prefix']

        self.stdout.write('username,password,user_id,token')

        for index in range(1, count + 1):
            username = f'{prefix}_{index}'
            email = f'{username}@example.com'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email},
            )

            user.email = email
            user.set_password(password)
            user.save(update_fields=['email', 'password'])

            token, _ = Token.objects.get_or_create(user=user)
            status = 'created' if created else 'updated'
            self.stdout.write(
                f'{username},{password},{user.id},{token.key} # {status}'
            )
