from django import template
from ShopApp.models import Product

register = template.Library()


@register.simple_tag
def filter_products():
    return Product.objects.filter(price__lt=10000)