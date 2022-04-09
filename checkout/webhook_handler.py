from django.http import HttpResponse


class StripeHandler:
    """Event handler for stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handler for unknown events
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handler for payment_intent.succeeded
        """
        intent = event.data.object
        print(intent)
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handler for payment_intent.payment_failed
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)