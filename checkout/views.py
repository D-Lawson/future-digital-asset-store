from decimal import Decimal
from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

import stripe
import json

from basket.contexts import basket_contents
from assets.models import Asset
from accounts.models import UserAccount
from accounts.forms import UserAccountForm
from .forms import OrderForm
from .models import Order, OrderLineItem


@require_POST
def cache_checkout_data(request):
    """ Cache checkout data """
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'basket': json.dumps(request.session.get('basket', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Apologies, but your transaction \
            cannot be processed at the moment. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    """ View for rendering to the checkout template """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        basket = request.session.get('basket', {})

        collect_form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'address_line_1': request.POST['address_line_1'],
            'address_line_2': request.POST['address_line_2'],
            'county': request.POST['county'],
        }
        create_order = OrderForm(collect_form_data)
        if create_order.is_valid():
            order = create_order.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_basket = json.dumps(basket)
            order.save()
            physical_item = False
            for asset_id, asset_data in basket.items():
                if not isinstance(asset_data, int):
                    for size, quantity in asset_data['asset_by_size'].items():
                        if size != 'Digital only':
                            physical_item = True
                    if physical_item:
                        order.delivery_cost = Decimal(3.99)
                    else:
                        order.delivery_cost = Decimal(0)
            create_order.save()

            for asset_id, asset_data in basket.items():
                try:
                    asset = Asset.objects.get(id=asset_id)
                    if isinstance(asset_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            asset=asset,
                            quantity=asset_data,
                        )
                        order_line_item.save()
                    else:
                        physical_item = False
                        for size, quantity in asset_data['asset_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                asset=asset,
                                quantity=quantity,
                                asset_size=size,
                            )
                            order_line_item.save()
                except Asset.DoesNotExist:
                    messages.error(request, (
                        "A checkout asset wasn't found in our database"
                        "Please contact us to address the issue")
                    )
                    order.delete()
                    return redirect(reverse('view_basket'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_completed',
                                    args=[order.order_id]))
        else:
            messages.error(request, 'An error has occurred with the form. \
                Please revise the form data inputted.')
    else:
        basket = request.session.get('basket', {})
        if not basket:
            messages.error(request, "Your basket is currently empty")
            return redirect(reverse('assets'))

        current_basket = basket_contents(request)
        total = current_basket['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        if request.user.is_authenticated:
            try:
                account = UserAccount.objects.get(user=request.user)
                create_order = OrderForm(initial={
                    'full_name': account.user.get_full_name(),
                    'email': account.user.email,
                    'phone_number': account.default_phone_number,
                    'country': account.default_country,
                    'postcode': account.default_postcode,
                    'town_or_city': account.default_town_or_city,
                    'address_line_1': account.default_address_line_1,
                    'address_line_2': account.default_address_line_2,
                    'county': account.default_county,
                })
            except UserAccount.DoesNotExist:
                create_order = OrderForm()
        else:
            create_order = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing from \
            environment')

    template = 'checkout/checkout.html'
    context = {
        'create_order': create_order,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_completed(request, order_id):
    """
    Process a valid checkout
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_id=order_id)

    if request.user.is_authenticated:
        account = UserAccount.objects.get(user=request.user)
        order.user_account = account
        order.save()

        if save_info:
            account_data = {
                'default_phone_number': order.phone_number,
                'default_country': order.country,
                'default_postcode': order.postcode,
                'default_town_or_city': order.town_or_city,
                'default_address_line_1': order.address_line_1,
                'default_address_line_2': order.address_line_2,
                'default_county': order.county,
            }
            user_account_form = UserAccountForm(account_data, instance=account)
            if user_account_form.is_valid():
                user_account_form.save()

    messages.success(request, f'Your order was a success! \
        The order number is {order_id}. An email \
        will be sent to {order.email} with confirmation.')

    if 'basket' in request.session:
        del request.session['basket']

    template = 'checkout/checkout_completed.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
