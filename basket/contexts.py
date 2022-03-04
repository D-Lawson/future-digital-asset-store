from django.conf import settings

def basket_contents(request):

    """ Function for handling contexts for basket contents """

    basket_items = []
    total = 0
    asset_count = 0
    discount = 0

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