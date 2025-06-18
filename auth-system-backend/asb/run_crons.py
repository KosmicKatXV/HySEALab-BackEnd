from datetime import timedelta
from django.core.management.base import BaseCommand
from django.db.models.functions import Now
from asb.models import CustomUser

class RemoveOldUsers(BaseCommand):
    help = 'Remove expired verification tokens'

    def handle(self, *args, **options):
        list = CustomUser._base_manager.filter(
            date_created__lt=Now()-timedelta(days=14),
            is_superuser=False
        )
        print(list)