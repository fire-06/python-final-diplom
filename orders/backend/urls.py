from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # Путь для получения токена авторизации
    path('api/v1/token/', obtain_auth_token, name='api_token_auth'),

    # Путь для регистрации пользователя
    path('api/v1/user/register/', views.UserRegistrationView.as_view(), name='user-register'),

    # Путь для импорта товаров (если нужно)
    path('api/v1/product/import/', views.ProductImport.as_view(), name='product-import'),

    # Путь для работы с продуктами
    path('api/v1/products/', views.ProductListView.as_view(), name='product-list'),
    path('api/v1/products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),

    # Путь для корзины
    path('api/v1/cart/', views.CartView.as_view(), name='cart'),

    # Путь для подтверждения заказа
    path('api/v1/order/confirm/<int:order_id>/', views.OrderConfirmationView.as_view(), name='order-confirm'),

    # Путь для списка заказов
    path('api/v1/orders/', views.OrderListView.as_view(), name='order-list'),

    # Путь для деталей заказа
    path('api/v1/orders/<int:order_id>/', views.OrderDetailView.as_view(), name='order-detail'),

    # Путь для страницы благодарности
    path('api/v1/thank-you/', views.ThankYouView.as_view(), name='thank-you'),
]
