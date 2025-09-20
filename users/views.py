from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view

from users.models import User
from users.serializers import UserSerializer


# Create your views here.
from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response
from .utils import get_cache_key


def get_cache_key(prefix, identifier=None):
    """Generate consistent cache keys"""
    if identifier:
        return f"{prefix}_{identifier}"
    return prefix


def list(self, request, *args, **kwargs):
    """
    Cached list method for DRF ViewSet.
    Caches results uniquely per query params and model.
    """
    # Step 1: Generate unique cache key using query params
    query_string = "_".join(f"{k}-{v}" for k, v in sorted(request.query_params.items()))
    cache_key = get_cache_key(f"{self.basename}_list", query_string or None)

    # Step 2: Try fetching cached data
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return Response(cached_data)

    # Step 3: Get fresh data from the original method
    response = super().list(request, *args, **kwargs)

    # Step 4: Store the serialized data in cache
    cache_timeout = getattr(settings, 'CACHE_TTL', 300)  # Default 5 minutes
    cache.set(cache_key, response.data, timeout=cache_timeout)

    return response
 

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        cache.delete('br4_key')  # Invalidate user list cache on create
        super().perform_create(serializer)
    
    def perform_update(self, serializer):
        user_id = serializer.instance.id
        cache.delete('br4_key')  # Invalidate user list cache on update
        cache.delete(f'br4_{user_id}')  # Invalidate individual user cache on update
        super().perform_update(serializer)
        user_data = self.get_serializer(serializer.instance).data
        cache_key = f"br4_{serializer.instance.id}"
        cache.set(cache_key, user_data, timeout=settings.CACHE_TTL)

@api_view(['GET'])
def cache_stats(request):
    from django.core.cache import cache
    import redis
    # Connect to Redis DB 1 (as per your settings)
    r = redis.Redis(host='127.0.0.1', port=6379, db=1)
    keys = r.keys('*')
    key_list = [k.decode('utf-8') for k in keys]
    total_keys = len(key_list)
    # Optionally, check if 'br4_key' is present and its value
    br4_key_value = cache.get('br4_key')
    return Response({
        'cache_keys': key_list,
        'total_keys': total_keys,
        'br4_key_present': 'br4_key' in key_list,
        'br4_key_value': br4_key_value,
    })