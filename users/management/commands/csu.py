from django.core.management import BaseCommand

from django.contrib.auth import get_user_model


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.get(email="admin@example.com").delete()
        user = User.objects.create(
            email="admin@example.com",
        )
        user.set_password("123qwe456rty")
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(
            self.style.SUCCESS(f"Суперпользователь успешно создан с email {user.email}")
        )
