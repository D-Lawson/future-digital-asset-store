from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_assets, name='assets'),
    path('<int:asset_id>/', views.asset_detail, name='asset_detail'),
    path('add/', views.add_asset, name='add_asset'),
    path('edit/<int:asset_id>/', views.edit_asset, name='edit_asset'),
    path('delete/<int:asset_id>/', views.delete_asset, name='delete_asset'),
]
