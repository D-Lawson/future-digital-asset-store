from django.contrib import admin
from .models import Asset, Category

# Register your models here.

class AssetAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'popularity',
        'image',
    )

    ordering = ('popularity',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'display_name',
        'name',
    )


admin.site.register(Asset, AssetAdmin)
admin.site.register(Category, CategoryAdmin)