from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_basket, name='view_basket'),
    path('add/<asset_id>/', views.add_to_basket, name='add_to_basket'),
    path('update/<asset_id>/', views.update_basket, name='update_basket'),
    path('remove/<asset_id>/', views.remove_asset, name='remove_asset'),
]