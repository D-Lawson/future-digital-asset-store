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
    qualify_discount = 0
    basket = request.session.get('basket', {})
    delivery = 0

    for asset_id, asset_data in basket.items():
        if isinstance(asset_data, int):
            asset = get_object_or_404(Asset, pk=asset_id)
            total += asset_data * asset.price
            asset_count += asset_data
            basket_items.append({
                'asset_id': asset_id,
                'asset': asset,
                'quantity': asset_data,
            })
        else:
            asset = get_object_or_404(Asset, pk=asset_id)
            for size, quantity in asset_data['asset_by_size'].items():
                if size != "Digital only":
                    delivery = Decimal(3.99)
                total += quantity * asset.price
                asset_count += quantity
                basket_items.append({
                    'asset_id': asset_id,
                    'asset': asset,
                    'quantity': quantity,
                    'size': size,
                })

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

    print(request.session.get('basket'))

    return context
