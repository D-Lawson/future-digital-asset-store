from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from assets.models import Asset


def basket_contents(request):

    """ Function for handling contexts for basket contents """

    basket_items = []
    total = 0
    asset_count = 0
    discount = 0
    basket = request.session.get('basket', {})
    qualify_discount = 0
    delivery = 0
    quantity = 1

    any_printed = list(basket.values())
    if 'Yes' in any_printed:
        delivery = Decimal(3.99)
    else:
        delivery = 0

    print_qty = any_printed.count("Yes")
    
    print(print_qty)

    for asset_id, printed in basket.items():
        asset = get_object_or_404(Asset, pk=asset_id)
        total += quantity * asset.price
        asset_count += quantity
        subtotal = asset.price
        if 'Yes' in printed:
            subtotal = asset.price + Decimal(4.99)
        
        basket_items.append({
            'asset_id': asset_id,
            'asset': asset,
            'printed': printed,
            'subtotal': subtotal
        })

    total = total + (print_qty * Decimal(4.99))

    if total < settings.DISCOUNT_THRESHOLD:
        qualify_discount = settings.DISCOUNT_THRESHOLD - total
    else:
        discount = total * Decimal(0.15)

    grand_total = total - discount + delivery
    display_discount = "{:.2f}".format(discount)

    context = {
        'basket_items': basket_items,
        'total': total,
        'asset_count': asset_count,
        'qualify_discount': qualify_discount,
        'discount_threshold': settings.DISCOUNT_THRESHOLD,
        'display_discount': display_discount,
        'delivery': delivery,
        'grand_total': grand_total,

    }

    return context