from django.urls import path
from . import views

urlpatterns = [
    path('', views.account, name='account'),
    path('previous_orders/<order_id>',
         views.previous_orders, name='previous_orders')
]
