from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from checkout.webhook_handler import StripeHandler

import stripe


@require_POST
@csrf_exempt
def webhook(request):
    """Listener for stripe webhooks"""
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    except Exception as e:
        return HttpResponse(content=e, status=400)

    stripe_handler = StripeHandler(request)

    event_map = {
        'payment_intent.succeeded':
        stripe_handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed':
        stripe_handler.handle_payment_intent_payment_failed,
    }

    event_type = event['type']

    event_handler = event_map.get(event_type, stripe_handler.handle_event)

    response = event_handler(event)
    return response
