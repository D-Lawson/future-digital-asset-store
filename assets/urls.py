from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_assets, name='assets'),
    path('<asset_id>', views.asset_detail, name='asset_detail'),
]
