from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Product, Category, Subcategory, DefaultUser, CartItem, Cart, WishList, ProductImage
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404

# User = get_user_model()


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image',)


class ProductListSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'price','description', 'images', 'category')


class CartItemSerializer(serializers.ModelSerializer):
    price = serializers.ReadOnlyField(source='get_total_price')

    class Meta:
        model = CartItem
        fields = ('product', 'quantity', 'price')


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, write_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'items',)

    def create(self, validated_data):
        request = self.context.get('request')
        items = validated_data.pop('items')
        user = request.user
        cart = Cart.objects.create(user=user)
        for item in items:
            CartItem.objects.create(cart=cart, product=item['product'], amount=item['amount'])
        return cart


class FavoriteListSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True, read_only=True)

    class Meta:
        model = WishList
        fields = '__all__'


class DefaultUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultUser
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


