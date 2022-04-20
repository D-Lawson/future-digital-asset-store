from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    """ Admin customisation for OrderLineItemAdminInline """
    model = OrderLineItem
    readonly_fields = ('total_sum',)


class OrderAdmin(admin.ModelAdmin):
    """ Admin customisation for OrderAdmin """

    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_id', 'date',
                       'delivery_cost', 'discount_amount', 'order_total',
                       'grand_total', 'original_basket', 'stripe_pid')

    fields = ('order_id', 'user_account', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'address_line_1',
              'address_line_2', 'county',
              'order_total', 'delivery_cost', 'discount_amount', 'grand_total',
              'original_basket', 'stripe_pid')

    list_display = ('order_id', 'date', 'full_name',
                    'order_total', 'delivery_cost', 'discount_amount',
                    'grand_total',)

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
