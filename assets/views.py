from django.shortcuts import render, get_object_or_404
from .models import Asset


def all_assets(request):
    """ Displays all assets with sorting and searching features """

    assets = Asset.objects.all()

    context = {
        'assets': assets,
    }

    return render(request, 'assets/assets.html', context)


def asset_detail(request, asset_id):
    """ Displays individual assets """

    asset = get_object_or_404(Asset, pk=asset_id)

    context = {
        'asset': asset,
    }

    return render(request, 'assets/asset_detail.html', context)
    