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
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer