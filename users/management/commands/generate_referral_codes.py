from django.core.management.base import BaseCommand
from users.models import UserProfile
import uuid

class Command(BaseCommand):
    help = 'Generate referral codes for all user profiles missing one.'

    def handle(self, *args, **options):
        count = 0
        for profile in UserProfile.objects.filter(referral_code__isnull=True):
            profile.referral_code = str(uuid.uuid4())[:8]
            profile.save()
            count += 1
        self.stdout.write(self.style.SUCCESS(f'Generated referral codes for {count} user profiles.'))
