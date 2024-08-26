from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(email="admin@gmail.com").exists():
            user = User.objects.create(email="admin@gmail.com")
            user.set_password("123qwe456rty")
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(self.style.SUCCESS("Удача"))
        else:
            self.stdout.write(self.style.WARNING("Фиг тебе"))
