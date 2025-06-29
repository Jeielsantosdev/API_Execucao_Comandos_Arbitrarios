from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
class Command(BaseCommand):
    help = 'Create a superuser with default credentials'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = 'admin'
        password = 'admin#2023'
        email = 'admin@gmail.com'
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                password=password,
                email=email
            )
            self.stdout.write(self.style.SUCCESS(
                f'Superuser {username} created successfully.'
            ))
        else:
            self.stdout.write(self.style.WARNING(
                f'Superuser {username} already exists.'
            ))