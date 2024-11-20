from django.core.management import BaseCommand
from users.models import User
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email="admin@example.com",
        )
        user.set_password("123qwe456rty")
        user.is_staff = True
        user.is_superuser = True
        user.save()
