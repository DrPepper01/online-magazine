from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import post_save, post_delete
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify

from ShopApp.signals import update_cart_total_price


class Administrator(models.Model):
    name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = PhoneNumberField()
    email_address = models.EmailField()
    password = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.name} {self.last_name}'


class DefaultUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # name = models.CharField(max_length=150)
    # last_name = models.CharField(max_length=150)
    # email = models.EmailField()
    # password = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    phone_number = PhoneNumberField()

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Category(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=70, primary_key=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Subcategory(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product/', blank=True, null=True)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    # items = models.ManyToManyField(Product, through='CartItem')
    # total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'Cart for user {self.user.first_name}'

    # def save(self, *args, **kwargs):
    #     # Сначала сохраняем объект Cart, чтобы у него был установлен первичный ключ
    #     super().save(*args, **kwargs)
    #
    #     # Calculate total price based on items in the cart
    #     total_price = sum(item.product.price * item.quantity for item in self.cartitem.all())
    #
    #     # Set total_price to 0 if the cart is empty
    #     self.total_price = total_price if total_price else 0
    #
    #     super().save(*args, **kwargs)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitem')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cartitem')
    quantity = models.PositiveIntegerField(default=1)
    # price = models.IntegerField()

    def __str__(self):
        return f'{self.quantity} of {self.product.title} in cart'

    def get_total_price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    user = models.ForeignKey(DefaultUser, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100,     choices=[
        ('Создан', 'Создан'),
        ('Заказ обрабатывается', 'Заказ обрабатывается'),
        ('Ожидает оплаты', 'Ожидает оплаты'),
        ('Оплачен', 'Оплачен'),
        ('Подтвержден', 'Подтвержден'),
        ('Готов к выдаче', 'Готов к выдаче'),
        ('Завершен', 'Завершен'),
    ])
    payment_method = models.CharField(max_length=100)
    shipping_method = models.CharField(max_length=100, choices=[('Pickup', 'Самовывоз'), ('Delivery', 'Доставка')])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    # def __str__(self):
    #     return f'Order {self.order_number} for user {self.user.first_name}'


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')
    favorite = models.BooleanField(default=False)

    def __str__(self):
        return str(f"{self.user} liked {self.product}")
