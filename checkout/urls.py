from django.urls import path
from . import views
from .webhooks import webhook


urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout_completed/<order_id>',
         views.checkout_completed, name='checkout_completed'),
    path('wh/', webhook, name='webhook'),
]
