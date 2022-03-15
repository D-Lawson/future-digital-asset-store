from django.test import TestCase

from .models import Order


class TestOrderModel(TestCase):
    def test_order_model(self):
        order = Order.objects.create()
    
        self.assertEqual(order.)