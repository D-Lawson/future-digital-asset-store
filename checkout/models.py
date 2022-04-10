import uuid
from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from assets.models import Asset
from accounts.models import UserAccount


class Order(models.Model):
    """ Model for creating an order"""
    order_id = models.CharField(max_length=32, null=False, editable=False)
    user_account = models.ForeignKey(UserAccount, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='orders')
    date = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    address_line_1 = models.CharField(max_length=80, null=False, blank=False)
    address_line_2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    county = models.CharField(max_length=80, null=True, blank=True)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    discount_amount = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    original_basket = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default='')

    def _generate_random_number(self):
        """
        Generate order number randomly with uuid
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total when items are added (factoring in discount and
         delivery)
        """
        self.order_total = self.lineitems.aggregate(Sum('total_sum'))[
            'total_sum__sum'] or 0

        if self.order_total < settings.DISCOUNT_THRESHOLD:
            self.discount_amount = Decimal(0)
        else:
            self.discount_amount = Decimal(self.order_total) * Decimal(0.15)

        self.grand_total = self.order_total + self.delivery_cost - \
            self.discount_amount
        self.save()

    def save(self, *args, **kwargs):
        """
        Set the order number if it hasn't yet been determined
        """
        if not self.order_id:
            self.order_id = self._generate_random_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_id


class OrderLineItem(models.Model):
    """ Order line item """
    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE,
                              related_name='lineitems')
    asset = models.ForeignKey(
        Asset, null=False, blank=False, on_delete=models.CASCADE)
    asset_size = models.CharField(max_length=25, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    total_sum = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Update the total in light of the changes made to basket
        """
        self.total_sum = self.asset.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'No {self.asset.pk} for order {self.order.order_id}'
