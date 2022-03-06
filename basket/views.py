from django.shortcuts import render, redirect

# Create your views here.


def view_basket(request):
    """ Renders the basket template with its contents """
    return render(request, 'basket/basket.html')


def add_to_basket(request, asset_id):
    """ Adds asset to basket """

    quantity = 1
    redirect_url = request.POST.get('redirect_url')
    basket = request.session.get('basket', {})

    basket[asset_id] = quantity

    request.session['basket'] = basket
    return redirect(redirect_url)