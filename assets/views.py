from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Asset, Category


def all_assets(request):
    """ Displays all assets with sorting and searching features """

    assets = Asset.objects.all()
    query = None
    categories = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            assets = assets.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

    if request.GET:
        if 'search' in request.GET:
            query = request.GET['search']
            if not query:
                messages.error(request, "Please enter a search criteria")
                return redirect(reverse('assets'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            assets = assets.filter(queries)

    context = {
        'assets': assets,
        'search_criteria': query,
        'current_categories': categories,
    }

    return render(request, 'assets/assets.html', context)


def asset_detail(request, asset_id):
    """ Displays individual assets """

    asset = get_object_or_404(Asset, pk=asset_id)

    context = {
        'asset': asset,
    }

    return render(request, 'assets/asset_detail.html', context)
    