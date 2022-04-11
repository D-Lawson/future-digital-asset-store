from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from assets.models import Asset
from accounts.models import UserAccount
from .models import Order, OrderLineItem

import json
import time


class StripeHandler:
    """Event handler for stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_email(self, order):
        """Send email confirming order details"""
        customer_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
        
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
        ) 

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
        pid = intent.id
        basket = intent.metadata.basket
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Update profile information if save_info was checked
        account = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            account = UserAccount.objects.get(user__username=username)
            if save_info:
                account.default_phone_number = shipping_details.phone
                account.default_country = shipping_details.address.country
                account.default_postcode = shipping_details.address.postal_code
                account.default_town_or_city = shipping_details.address.city
                account.default_address_line_1 = shipping_details.address.line1
                account.default_address_line_2 = shipping_details.address.line2
                account.default_county = shipping_details.address.state
                account.save()

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    address_line_1__iexact=shipping_details.address.line1,
                    address_line_2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_basket=basket,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            self._send_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Order matches original basket',
                status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    user_account=account,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    address_line_1=shipping_details.address.line1,
                    address_line_2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    original_basket=basket,
                    stripe_pid=pid,
                )
                for asset_id, asset_data in json.loads(basket).items():
                    asset = Asset.objects.get(id=asset_id)
                    if isinstance(asset_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            asset=asset,
                            quantity=asset_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in asset_data['asset_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                asset=asset,
                                quantity=quantity,
                                asset_size=size,
                            )
                            order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        self._send_email(order)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Order \
            created with webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handler for payment_intent.payment_failed
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
