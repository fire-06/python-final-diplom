from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import (
    UserSerializer,
    ProductSerializer,
    ProductInfoSerializer,
    ParameterSerializer,
    ProductParameterSerializer,
    OrderSerializer,
    UserRegistrationSerializer,
    CartSerializer,
    CartItemSerializer,
)
from .models import User, Shop, Category, Product, ProductInfo, Parameter, ProductParameter, Order, Cart, CartItem


class UserRegistrationView(APIView):
    """
    Представление для регистрации пользователя.
    """
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartView(APIView):
    """
    Представление для работы с корзиной.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=request.user)
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response({"detail": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemView(APIView):
    """
    Представление для добавления товаров в корзину.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductInfoView(APIView):
    """
    Представление для получения информации о товарах.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        product_info = ProductInfo.objects.all()
        serializer = ProductInfoSerializer(product_info, many=True)
        return Response(serializer.data)


class ProductListView(APIView):
    """
    Представление для списка продуктов.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetailView(APIView):
    """
    Представление для детализации продукта.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(pk=kwargs['pk'])
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


class OrderListView(APIView):
    """
    Представление для списка заказов.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderDetailView(APIView):
    """
    Представление для детализации заказа.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(id=kwargs['order_id'], user=request.user)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)


class OrderConfirmationView(APIView):
    """
    Представление для подтверждения заказа.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(id=kwargs['order_id'], user=request.user)
            order.state = 'confirmed'
            order.save()
            return Response({"detail": "Order confirmed"}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)


class ThankYouView(APIView):
    """
    Представление для страницы благодарности после оформления заказа.
    """
    def get(self, request, *args, **kwargs):
        return Response({"message": "Thank you for your order!"}, status=status.HTTP_200_OK)


class ProductImport(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Логика импорта товаров
        return Response({"message": "Products imported successfully"}, status=status.HTTP_200_OK)