from django.shortcuts import render
from .models import Asset


def all_assets(request):
    """ Displays all assets with sorting and searching features """

    assets = Asset.objects.all()

    context = {
        'assets': assets,
    }

    return render(request, 'assets/assets.html', context)
