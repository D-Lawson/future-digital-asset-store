
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem


@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update the order total when changes are made to order
    """
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update the order total when item is removed
    """
    instance.order.update_total()


@receiver(post_save, sender=OrderLineItem)
def update_asset_on_save(sender, instance, **kwargs):
    """
    Increment the asset popularity on purchase
    """
    instance.asset.increment_popularity()
