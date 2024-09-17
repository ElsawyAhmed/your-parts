from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .utils import get_cart
from .serializers import *
from django.db import transaction

from rest_framework.generics import (CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView)

class RegisterCustomerView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Account created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Product API Views
class ProductCreateAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class ProductRetrieveAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class ProductDeleteAPIView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductEditAPIView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderListAPIView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderRetrieveAPIView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
#
class OrderEditAPIView(UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    #//// todo: update the value of product stock if an order updated
    """
    Case cancelled -- return quantity to stock 
    """






@api_view(['GET'])
@permission_classes([])
def get_cart_view(request):
    cart = get_cart(request)
    cart_serializer = CartSerializer(cart)
    return Response(cart_serializer.data)

@api_view(['POST'])
@permission_classes([])
def add_to_cart_view(request):
    cart = get_cart(request)
    print("Cart", cart)
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += quantity
    if cart_item.quantity > product.stock:
        return Response({"error": "Quantity required is not available now"}, status=403)
    cart_item.save()

    return Response({"message": "Product added to cart"})


# Update item quantity in a cart
@api_view(['DELETE'])
@permission_classes([])
def remove_from_cart_view(request, item_id):
    cart = get_cart(request)
    try:
        cart_item = CartItem.objects.get(cart=cart, product=item_id)
        cart_item.delete()
        return Response({"message": "Item removed from cart."}, status=status.HTTP_200_OK)
    except CartItem.DoesNotExist:
        return Response({"error": "Item not found in cart."}, status=status.HTTP_404_NOT_FOUND)


# Delete an item from cart
@api_view(['PUT'])
@permission_classes([])
def update_cart_item_quantity_view(request, item_id):
    cart = get_cart(request)
    try:
        print("in try")
        cart_item = CartItem.objects.get(cart=cart, product=item_id)
        print(cart_item)
    except CartItem.DoesNotExist as e:
        print(e)
        return Response({"error": "Item not found in cart."}, status=status.HTTP_404_NOT_FOUND)

    serializer = CartItemUpdateSerializer(cart_item, data=request.data)
    if serializer.is_valid():
        if serializer.validated_data['quantity'] == 0:
            cart_item.delete()
            return Response({"message": "Item removed from cart."}, status=status.HTTP_200_OK)
        else:
            serializer.save()
            return Response({"message": "Cart item quantity updated."}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# Order Checkout
@api_view(['POST'])
@transaction.atomic
@permission_classes([])
def checkout_view(request):
    # Get cart (either for authenticated user or guest)
    cart = get_cart(request)

    if cart.items.count() == 0:
        return Response({"error": "Cart is empty"}, status=400)

    # Create the order
    if request.user.is_authenticated:
        order = Order.objects.create(user=request.user, total_price=0)
    else:
        session_id = request.session.session_key
        order = Order.objects.create(session_id=session_id, total_price=0)

    # Move cart items to order items
    total_price = 0
    for cart_item in cart.items.all():
        order_item = OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )
        # subtract the order product amount from stock
        cart_item.product.stock -= cart_item.quantity
        cart_item.product.save()
        total_price += cart_item.product.price * cart_item.quantity

    # Update the order with the total price
    order.total_price = total_price
    order.save()

    # Clear the cart
    cart.items.all().delete()

    # Return the order information (serialized)
    order_serializer = OrderSerializer(order)
    return Response(order_serializer.data)