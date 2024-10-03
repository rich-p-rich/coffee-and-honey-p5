from django import template


register = template.Library()

@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    price = price if price is not None else 0.0
    quantity = quantity if quantity is not None else 0
    return price * quantity