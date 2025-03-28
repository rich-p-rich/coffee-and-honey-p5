from django.contrib import admin
from .models import Order, OrderLineItem

# Register your models here.


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total', 'original_bag',
                       'stripe_pid')

    fields = ('order_number', 'date', 'billing_full_name', 'billing_email',
              'billing_phone_number', 'billing_country', 'billing_postcode',
              'billing_town_or_city', 'billing_street_address1',
              'billing_street_address2', 'billing_county', 'delivery_cost',
              'order_total', 'grand_total', 'original_bag', 'stripe_pid')

    list_display = ('order_number', 'date', 'billing_full_name', 'order_total',
                    'delivery_cost', 'grand_total')

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
