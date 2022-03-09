from django.shortcuts import render, redirect

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
