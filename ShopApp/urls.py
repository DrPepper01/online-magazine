from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import BaseTemplateView, ProductViewSet, HomeTemplateView, ProductDetailView, CartView, update_quantity, \
    CategoryDetailView, DestroyProductView, ProductCreateView, ProductUpdateView, DeleteProductView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='API ',
        default_version='v1',
        description='Test',
        terms_of_service='',
        contact=openapi.Contact(email=''),
        license=openapi.License(name='')
    ),
    public=True
)


router = DefaultRouter()
router.register(r'category', views.CategoryViewSet)
router.register(r'subcategory', views.SubcategoryViewSet, basename='subcategory')
router.register(r'product', views.ProductViewSet)
router.register(r'cart-vewset', views.CartViewSet)

# router.register('api/update-product', views.UpdateAPIView, basename='update-product')
# router.register('api/delete-product', views.DeleteAPIView, basename='delete-product')
# router.register('favorite', views.FavoriteView)


urlpatterns = [
    path(r'base/', BaseTemplateView.as_view(), name='base_template'),
    path(r'product/search/', ProductViewSet.as_view({'get': 'search'}), name='search_view'),
    path(r'products_list/', HomeTemplateView.as_view(), name='products'),
    path(r'products_list/<int:pk>', ProductDetailView.as_view(), name='products_detail'),
    path(r'cart/', CartView.as_view(), name='cart_view'),
    path(r'update_quantity/<int:cart_item_id>/', update_quantity, name='update_quantity'),
    # path('base/', CategoryListView.as_view(), name='category_list'),
    path(r'categories/<slug:category_slug>/', CategoryDetailView.as_view(), name='category_detail'),
    # path('product/search/', views.product_search, name='product_search'),

    path(r'token/', TokenObtainPairView.as_view(), name='api_login'),
    path(r'token/refresh/', TokenRefreshView.as_view(), name='api_refresh'),
    path(r'auth/', views.authenticate_user),

    path(r'api/create-product', views.ProductCreateView.as_view(), name='api-create-product'),
    path(r'api/update-product/<int:pk>', views.UpdateProductView.as_view(), name='api-update-product'),
    path(r'api/products/<int:pk>/delete', DestroyProductView.as_view(), name='api-product_delete'),

    path(r'products/create', ProductCreateView.as_view(), name='product_create'),
    path('products_list/<int:pk>/update', ProductUpdateView.as_view(), name='product_detail'),
    path('products_list/<int:pk>/delete', DeleteProductView.as_view(), name='product_delete'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_ui'),



    # path('publishers/<int:pk>', views.get_publisher, name='book_publisher_detain'),
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_ui'),
    # path('token/', TokenObtainPairView.as_view(), name='api_login'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='api_refresh'),
    # path('create_user/', views.CreateUserView.as_view()),
    # path('auth/', views.authenticate_user)
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)