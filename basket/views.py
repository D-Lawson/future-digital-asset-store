from django.shortcuts import render, redirect, reverse, HttpResponse

# Create your views here.


def view_basket(request):
    """ Renders the basket template with its contents """
    return render(request, 'basket/basket.html')


def add_to_basket(request, asset_id):
    """ Adds asset to basket """

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
            else:
                basket[asset_id]['asset_by_size'][size] = quantity
        else:
            basket[asset_id] = {'asset_by_size': {size: quantity}}
    else:
        if asset_id in list(basket.keys()):
            basket[asset_id] += quantity
        else:
            basket[asset_id] = quantity

    request.session['basket'] = basket
    print(request.session['basket'])
    return redirect(redirect_url)


def update_basket(request, asset_id):
    """ Update quantity within basket """

    quantity = int(request.POST.get('quantity'))

    size = None
    if 'print_size' in request.POST:
        size = request.POST['print_size']

    basket = request.session.get('basket', {})

    if size:
        if quantity > 0:
            basket[asset_id]['asset_by_size'][size] = quantity
        else:
            del basket[asset_id]['asset_by_size'][size]
            if not basket[asset_id]['asset_by_size']:
                basket.pop(asset_id)
    else:
        if quantity > 0:
            basket[asset_id] = quantity
        else:
            basket.pop(asset_id)

    request.session['basket'] = basket
    print(request.session['basket'])
    return redirect(reverse('view_basket'))


def remove_asset(request, asset_id):
    """ Remove asset from basket """

    try:
        size = None
        if 'print_size' in request.POST:
            size = request.POST['print_size']

        basket = request.session.get('basket', {})

        if size:
            del basket[asset_id]['asset_by_size'][size]
            if not basket[asset_id]['asset_by_size']:
                basket.pop(asset_id)
        else:
            basket.pop(asset_id)

        request.session['basket'] = basket
        return HttpResponse(status=200)
        
    except Exception as e:
        return HttpResponse(status=500)