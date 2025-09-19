from django.shortcuts import render
from rest_framework import viewsets

from users.models import User
from users.serializers import UserSerializer


# Create your views here.
  from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response


def get_cache_key(prefix, identifier=None):
    """Generate consistent cache keys"""
    if identifier:
        return f"{prefix}_{identifier}"
    return prefix

   from django.core.cache import cache
from rest_framework.response import Response
from .utils import get_cache_key
from django.conf import settings

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