from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@receiver(post_save, sender='ShopApp.CartItem')
@receiver(post_delete, sender='ShopApp.CartItem')
def update_cart_total_price(sender, instance, **kwargs):
    # Получаем корзину, связанную с CartItem
    cart = instance.cart
    from ShopApp.models import CartItem
    # Пересчитываем total_price
    total_price = sum(item.product.price * item.quantity for item in cart.cartitem.all())

    # Устанавливаем total_price для корзины
    cart.total_price = total_price if total_price else 0

    # Сохраняем изменения в корзине
    cart.save()
