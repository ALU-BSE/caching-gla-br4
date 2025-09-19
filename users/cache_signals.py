from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import User

@receiver(post_save, sender=User)
def invalidate_user_cache(sender, instance, **kwargs):
    cache.delete('br4_key')  # Invalidate user list cache
    cache.delete(f'br4_{instance.id}')  # Invalidate individual user cache
    pass

@receiver(post_delete, sender=User)  
def invalidate_user_cache_on_delete(sender, instance, **kwargs):
    cache.delete('br4_key')  # Invalidate user list cache
    cache.delete(f'br4_{instance.id}')  # Invalidate individual user cache
    pass