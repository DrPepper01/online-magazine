from django.contrib import admin
from .models import *


admin.site.register(Administrator)
admin.site.register(DefaultUser)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Product)
admin.site.register(WishList)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(ProductImage)
