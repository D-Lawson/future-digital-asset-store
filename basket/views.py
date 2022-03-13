from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from assets.models import Asset

# Create your views here.


def view_basket(request):
    """ Renders the basket template with its contents """
    return render(request, 'basket/basket.html')


def add_to_basket(request, asset_id):
    """ Adds asset to basket """

    asset = get_object_or_404(Asset, pk=asset_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')

    size = None
    if 'print_size' in request.POST:
        size = request.POST['print_size']

    basket = request.session.get('basket', {})

    if size:
        if asset_id in list(basket.keys()):
            if size in basket[asset_id]['asset_by_size'].keys():
                basket[asset_id]['asset_by_size'][size] += quantity
                messages.success(request, f'Updated {size.upper()} {asset.name} quantity to {basket[asset_id]["asset_by_size"][size]}')
            else:
                basket[asset_id]['asset_by_size'][size] = quantity
                messages.success(request, f'Great choice! Print size {size.upper()} for {asset.name} added to basket')
        else:
            basket[asset_id] = {'asset_by_size': {size: quantity}}
            messages.success(request, f'Great choice! Print size {size.upper()} for {asset.name} added to basket')
    else:
        if asset_id in list(basket.keys()):
            basket[asset_id] += quantity
            messages.success(request, f'Quantity updated for {asset.name} {basket[asset_id]}')
        else:
            basket[asset_id] = quantity
            messages.success(request, f'Great choice! {asset.name} added to basket')

    request.session['basket'] = basket
    print(request.session['basket'])
    return redirect(redirect_url)


def update_basket(request, asset_id):
    """ Update quantity within basket """

    asset = get_object_or_404(Asset, pk=asset_id)
    quantity = int(request.POST.get('quantity'))

    size = None
    if 'print_size' in request.POST:
        size = request.POST['print_size']

    basket = request.session.get('basket', {})

    if size:
        if quantity > 0:
            basket[asset_id]['asset_by_size'][size] = quantity
            messages.success(request, f'Updated {size.upper()} {asset.name} quantity to {basket[asset_id]["asset_by_size"][size]}')
        else:
            del basket[asset_id]['asset_by_size'][size]
            if not basket[asset_id]['asset_by_size']:
                basket.pop(asset_id)
            messages.success(request, f'{size.upper()} for {asset.name} removed from basket')

    else:
        if quantity > 0:
            basket[asset_id] = quantity
            messages.success(request, f'Quantity updated for {asset.name} - {basket[asset_id]}')
        else:
            basket.pop(asset_id)
            messages.success(request, f'{asset.name} removed from basket')

    request.session['basket'] = basket
    print(request.session['basket'])
    return redirect(reverse('view_basket'))


def remove_asset(request, asset_id):
    """ Remove asset from basket """

    asset = get_object_or_404(Asset, pk=asset_id)

    try:
        size = None
        if 'print_size' in request.POST:
            size = request.POST['print_size']

        basket = request.session.get('basket', {})

        if size:
            del basket[asset_id]['asset_by_size'][size]
            if not basket[asset_id]['asset_by_size']:
                basket.pop(asset_id)
            messages.success(request, f'{size.upper()} for {asset.name} removed from basket')
        else:
            basket.pop(asset_id)
            messages.success(request, f'{asset.name} removed from basket')

        request.session['basket'] = basket
        return HttpResponse(status=200)
        
    except Exception as e:
        message.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)