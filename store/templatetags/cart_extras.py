from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def sum_total(cart):
    return sum(item['total_price'] for item in cart)
