from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Comment)
def log_comment_action(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New comment added by {instance.name} with rating {instance.rating}")
    else:
        logger.info(f"Comment updated by {instance.name} with rating {instance.rating}")