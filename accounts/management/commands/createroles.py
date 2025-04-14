from django.core.management.base import BaseCommand
from accounts.models import create_roles as cr


class Command(BaseCommand):
    help = 'Creates calculator access roles in the system.'

    def handle(self, *args, **kwargs):
        cr()