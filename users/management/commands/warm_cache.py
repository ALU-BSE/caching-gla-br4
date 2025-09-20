from django.core.management.base import BaseCommand
from django.core.cache import cache
from users.models import User
from users.serializers import UserSerializer

class Command(BaseCommand):
    help = 'Warm up the cache with frequently accessed data'

    def handle(self, *args, **options):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        cache.set('br4_key', serializer.data, timeout=3600)
        for user in users:
            user_data = UserSerializer(user).data
            cache.set(f'br4_{user.id}', user_data, timeout=3600)
        self.stdout.write(
            self.style.SUCCESS(f'Successfully cached {len(users)} users')
        )