import os
import shutil
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from core.factories import UserFactory


class Command(BaseCommand):

    def ensure_clean_dir(self, folder):
        path = os.path.join(settings.MEDIA_ROOT, folder)
        if os.path.exists(path):
            shutil.rmtree(path)
        if not os.path.exists(path):
            os.makedirs(path)

    def handle(self, *args, **options):
        get_user_model().objects.all().delete()
        UserFactory(
            username='admin',
            is_staff=True,
            is_superuser=True
        )

        for i in range(3):
            UserFactory(username='user{}'.format(i))
