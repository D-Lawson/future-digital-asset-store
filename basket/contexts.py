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

    for asset_id, quantity in basket.items():
        asset = get_object_or_404(Asset, pk=asset_id)
        total += quantity * asset.price
        asset_count += quantity
        basket_items.append({
            'asset_id': asset_id,
            'quantity': quantity,
            'asset': asset,
        })

    if total < settings.DISCOUNT_THRESHOLD:
        qualify_discount = settings.DISCOUNT_THRESHOLD - total
    else:
        discount = total * 0.15

    grand_total = total - discount
    
    context = {
        'basket_items': basket_items,
        'total': total,
        'asset_count': asset_count,
        'qualify_discount': qualify_discount,
        'discount_threshold': settings.DISCOUNT_THRESHOLD,
        'grand_total': grand_total,
    }

    return context