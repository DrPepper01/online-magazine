from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from rest_framework import viewsets, permissions, status, filters, generics, response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action, api_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
import django_filters.rest_framework as filters
from rest_framework_simplejwt.tokens import RefreshToken

from . import throttles
from .filters import ProductFilter
from .forms import CustomAuthenticationForm, ProductForm
from .models import Product, Category, Subcategory, DefaultUser, WishList, Cart, CartItem
from .permissions import DenyAll
from .serializers import CategorySerializer, SubCategorySerializer, DefaultUserSerializer, \
    ProductListSerializer, CartSerializer, FavoriteListSerializer, UserSerializer


# Create your views here.


class BaseTemplateView(View):
    template_name = 'layouts/index.html'

    # def get(self, request):
    #     return render(request, self.template_name)

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        return render(request, self.template_name, {'categories': categories})

    throttle_classes = [
        throttles.CustomRateThrottle,
    ]

# def product_search(self,request, pk=None):
#     search_query = request.GET.get('q', '')
#     search_results = Product.objects.filter(title__icontains=search_query,
#                                             description__icontains=search_query)
#
#     return render(request, 'layouts/index.html', {'search_results': search_results})


# @method_decorator(csrf_protect, name='dispatch')
class HomeTemplateView(View):
    template_name = 'ShopApp/home_page.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        return render(request, self.template_name, {'categories': categories})



class ProductDetailView(DetailView):
    model = Product
    template_name = 'ShopApp/product_detail.html'
    context_object_name = 'product'






class ProductCreateView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class UpdateProductView(UpdateAPIView):
    serializer_class = ProductListSerializer

    def get_object(self):
        # Получаем объект по переданному в запросе идентификатору (pk)
        pk = self.kwargs.get('pk')
        return get_object_or_404(Product, pk=pk)

    def get(self, request, *args, **kwargs):
        # Добавьте логику получения данных, если нужно
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class DestroyProductView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, **kwargs):
        # Добавьте логику получения данных, если нужно
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'ShopApp/form.html'
    success_url = '/products/{id}'

    def get_context_data(self, **kwargs):
        '''

        :param kwargs:
        :return:
        '''
        context = super().get_context_data(**kwargs)
        context['value'] = 'Создание Товара'
        context['btn_value'] = 'Создать'
        return context

    def form_valid(self, form):
        """
        :is_valid() - проверяет коректность формы
        :redirect - внутри этой команды мы сначала переходим по первому значению
        затем туда вставляется наш PK и в это время мы применяем form.save()
        """
        if form.is_valid():
            firma = form.save()
            return redirect('products_detail', firma.pk)

    def form_invalid(self, form):
        '''

        :param form:
        :return:
        '''
        return HttpResponse('Что то пошло не так, Категория не была создана =(')


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'ShopApp/form.html'
    fields = '__all__'
    success_url = '/products_list/{id}'

    def get_context_data(self, **kwargs):
        '''

        :param kwargs:
        :return:
        '''
        context = super().get_context_data(**kwargs)
        context['value'] = 'Обновить товар'
        context['btn_value'] = 'Обновить'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        # Получаем PK только что созданного товара
        pk = self.object.pk
        # Формируем URL для перенаправления
        url = reverse('products_detail', kwargs={'pk': pk})
        return HttpResponseRedirect(url)

    def form_invalid(self, form):
        '''

        :param form:
        :return:
        '''
        return HttpResponse('Что то пошло не так, Категория не обновилась =(')


class DeleteProductView(DeleteView):
    '''

    '''
    model = Product
    template_name = 'ShopApp/form.html'
    success_url = reverse_lazy('products')
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        '''

        :param kwargs:
        :return:
        '''
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['product'] = product
        context['value'] = 'Удаление Товара'
        context['btn_value'] = 'Удалить'
        messages.warning(self.request, f'Вы хотите удалить товар {product}? ')
        return context


class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubCategorySerializer




class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_class = ProductFilter
    ordering_fields = ['title', 'price']

    throttle_classes = [
        throttles.CustomRateThrottle,
    ]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        elif self.action in ['create_review', 'like', 'favorites']:
            return [IsAuthenticated()]
        return []

    # api/v1/products/products/id/favorites/
    @action(detail=True, methods=['POST'])
    def favorites(self, request, pk):
        product = self.get_object()
        user = request.user
        fav, created = WishList.objects.get_or_create(product=product, user=user)
        if fav.favorite:
            fav.favorite = False
            fav.save()
            return Response('removed from favorites')
        else:
            fav.favorite = True
            fav.save()
            return Response('added to favorites')

    @action(detail=False, methods=["GET"])
    def search(self, request, pk=None):
        q = request.query_params.get("q")  # request.query_params = request.GET
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) |
                                   Q(description__icontains=q))

        serializer = ProductListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    throttle_classes = [
        throttles.CustomRateThrottle,
    ]

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update']:
            return [IsAdminUser()]
        else:
            return [DenyAll()]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset


class FavoriteView(ListAPIView):
    queryset = WishList.objects.all()
    serializer_class = FavoriteListSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}


# Views for Authorization


# class CustomLoginView(LoginView):
#     model = DefaultUser  # Укажите свою модель
#
#     template_name = 'your_login_template.html'  # Замените на свой шаблон
#     success_url = reverse_lazy('your_success_url')  # Замените на свой URL
#
#     def form_valid(self, form):
#         response = super().form_valid(form)
#         # Ваша логика, которая будет выполнена после успешной аутентификации
#         return response
#
#     def form_invalid(self, form):
#         response = super().form_invalid(form)
#         # Ваша логика, которая будет выполнена при ошибке аутентификации
#         return response


# Views for DefaultUser

class RegisterView(CreateAPIView):
    queryset = DefaultUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


class AuthWithToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id})

class DefaultUserViewSet(viewsets.ModelViewSet):
    queryset = DefaultUser.objects.all()
    serializer_class = DefaultUserSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


@api_view(['POST'])
def authenticate_user(request):
    try:
        user = request.data
        login = user['username']
        password = user['password']
        user = authenticate(request, username=login, password=password)
        token = RefreshToken.for_user(user)

        return Response({
            'refresh': str(token),
            'access': str(token.access_token)
        })
    except User.DoesNotExist or KeyError as e:
        print(e)
        return Response(status=404)


# views for Cart


class CartView(View):
    template_name = 'ShopApp/cart.html'

    def get(self, request, *args, **kwargs):
        # Получаем текущего пользователя
        user = request.user

        # Получаем корзину пользователя
        cart_items = CartItem.objects.filter(cart__user=user.id)

        # Считаем общую цену
        total_price = sum(item.get_total_price() for item in cart_items)

        context = {
            'cart_items': cart_items,
            'total_price': total_price,
        }

        return render(request, self.template_name, context)


def update_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)

    if request.method == 'POST':
        action = request.POST.get('action', None)

        if action == 'increment':
            cart_item.quantity += 1
        elif action == 'decrement':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1

        cart_item.save()

    return HttpResponseRedirect(reverse('cart_view'))


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'ShopApp/category_detail.html'  #
    context_object_name = 'category'
    slug_field = 'slug'  # Указываем, что мы используем поле slug для поиска категории
    slug_url_kwarg = 'category_slug'  # Указываем, как будет выглядеть slug в URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем текущую категорию
        category = self.get_object()

        # Передаем все категории в контекст
        context['categories'] = Category.objects.all()

        # Получаем все товары, связанные с текущей категорией
        context['products'] = Product.objects.filter(category=category)

        return context


class LoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'ShopApp/login.html'
