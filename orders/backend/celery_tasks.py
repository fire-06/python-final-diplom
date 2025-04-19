# backend/celery_tasks.py

from celery import shared_task
from django.contrib.auth import get_user_model
from backend.models import Shop, Category, Product, ProductInfo, Order, Cart, OrderItem, Contact

User = get_user_model()

@shared_task
def import_products(user_id, data):
    """
    Импортирует товары в магазин.
    """
    try:
        shop = Shop.objects.get(user_id=user_id)
    except Shop.DoesNotExist:
        return f"Error: Shop for user {user_id} not found"

    for item in data:
        category_name = item.get('category')
        product_name = item.get('name')
        model = item.get('model', '')
        external_id = item.get('external_id')
        quantity = item.get('quantity')
        price = item.get('price')
        price_rrc = item.get('price_rrc')

        if not all([category_name, product_name, external_id, quantity, price, price_rrc]):
            return f"Error: Missing required fields in item {item}"

        category, _ = Category.objects.get_or_create(name=category_name)
        category.shops.add(shop)

        product, _ = Product.objects.get_or_create(name=product_name, category=category)

        ProductInfo.objects.update_or_create(
            product=product,
            shop=shop,
            external_id=external_id,
            defaults={
                'model': model,
                'quantity': quantity,
                'price': price,
                'price_rrc': price_rrc
            }
        )

    return "Products imported successfully"

@shared_task
def create_order(user_id, contact_id):
    """
    Создает заказ из корзины пользователя.
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return f"Error: User {user_id} not found"

    try:
        contact = Contact.objects.get(id=contact_id, user=user)
    except Contact.DoesNotExist:
        return f"Error: Contact {contact_id} not found for user {user_id}"

    carts = Cart.objects.filter(user=user)
    if not carts.exists():
        return "Error: Cart is empty"

    order = Order.objects.create(user=user, contact=contact, state='new')

    for cart in carts:
        OrderItem.objects.create(
            order=order,
            product_info=cart.product_info,
            quantity=cart.quantity
        )

    carts.delete()
    return f"Order {order.id} created successfully"