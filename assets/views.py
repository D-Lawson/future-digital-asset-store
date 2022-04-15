from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Asset, Category
from .forms import AssetForm


def all_assets(request):
    """ Displays all assets with sorting and searching features """

    assets = Asset.objects.all()
    query = None
    categories = None
    direction = None
    sort = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                assets = assets.annotate(lower_name=Lower('name'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            assets = assets.order_by(sortkey)

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

            queries = Q(name__icontains=query) | Q(
                description__icontains=query)
            assets = assets.filter(queries)

    active_sort = f'{sort}_{direction}'

    context = {
        'assets': assets,
        'search_criteria': query,
        'active_categories': categories,
        'active_sort': active_sort,
    }

    return render(request, 'assets/assets.html', context)


def asset_detail(request, asset_id):
    """ Displays individual assets """

    asset = get_object_or_404(Asset, pk=asset_id)

    context = {
        'asset': asset,
    }

    return render(request, 'assets/asset_detail.html', context)


@login_required
def add_asset(request):
    """ Add new asset to collection """
    if not request.user.is_superuser:
        messages.error(request, 'You do not have site permissions to do that')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = AssetForm(request.POST, request.FILES)
        if form.is_valid():
            asset = form.save()
            messages.success(request, 'New asset added to collection.')
            return redirect(reverse('asset_detail', args=[asset.id]))
        else:
            messages.error(
                request, 'Please check that the form has been completed \
                    properly.')
    else:
        form = AssetForm()

    template = 'assets/add_asset.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_asset(request, asset_id):
    """ Edit existing asset details """
    if not request.user.is_superuser:
        messages.error(request, 'You do not have site permissions to do that')
        return redirect(reverse('home'))

    asset = get_object_or_404(Asset, pk=asset_id)
    if request.method == 'POST':
        form = AssetForm(request.POST, request.FILES, instance=asset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Asset has been updated')
            return redirect(reverse('asset_detail', args=[asset.id]))
        else:
            messages.error(request, 'Please check that the form has been completed \
                    properly.')
    else:
        form = AssetForm(instance=asset)
        messages.info(request, f'Currently editing {asset.name}')

    template = 'assets/edit_asset.html'
    context = {
        'form': form,
        'asset': asset,
    }

    return render(request, template, context)


@login_required
def delete_asset(request, asset_id):
    """ Delete an asset from the collection """
    if not request.user.is_superuser:
        messages.error(request, 'You do not have site permissions to do that')
        return redirect(reverse('home'))

    asset = get_object_or_404(Asset, pk=asset_id)
    asset.delete()
    messages.success(request, 'Asset deleted')
    return redirect(reverse('assets'))