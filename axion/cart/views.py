from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from .serializer import CartSerializer, CartItemSerializer


@api_view(["GET", "POST"])
def cart_list_create(request):
    if request.method == "GET":
        user_id = request.query_params.get("user_id")
        if not user_id:
            return Response({"error": "Missing user_id"}, status=400)

        try:
            cart = Cart.objects.get(customer_id=user_id)
        except Cart.DoesNotExist:
            return Response(
                {"detail": "Cart not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CartSerializer(cart)
        return Response(serializer.data)

    user_id = request.data.get("user_id")
    if not user_id:
        return Response({"error": "Missing user_id"}, status=400)

    data = request.data.copy()
    data["customer"] = user_id
    serializer = CartSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def cart_detail(request, cart_id):
    try:
        cart = Cart.objects.get(pk=cart_id, customer=request.user)
    except Cart.DoesNotExist:
        return Response({"detail": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = CartSerializer(cart, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    cart.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def cart_items_list_create(request, cart_id):
    try:
        cart = Cart.objects.get(pk=cart_id, customer=request.user)
    except Cart.DoesNotExist:
        return Response({"detail": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        items = cart.items.all()
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)

    data = request.data.copy()
    data["cart"] = cart_id
    serializer = CartItemSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def cart_item_detail(request, cart_id, cart_item_id):
    user_id = request.query_params.get("user_id") or request.data.get("user_id")
    if not user_id:
        return Response({"error": "Missing user_id"}, status=400)

    try:
        cart = Cart.objects.get(pk=cart_id, customer_id=user_id)
    except Cart.DoesNotExist:
        return Response({"detail": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        item = CartItem.objects.get(pk=cart_item_id, cart=cart)
    except CartItem.DoesNotExist:
        return Response({"detail": "Cart item not found"}, status=404)

    if request.method == "GET":
        serializer = CartItemSerializer(item)
        return Response(serializer.data)

    elif request.method == "PUT":
        data = request.data.copy()
        data["cart"] = cart_id
        serializer = CartItemSerializer(item, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    item.delete()
    return Response(status=204)


@api_view(["GET"])
def my_cart(request):
    user_id = request.query_params.get("user_id")
    if not user_id:
        return Response({"error": "Missing user_id"}, status=400)

    try:
        cart = Cart.objects.get(customer_id=user_id)
    except Cart.DoesNotExist:
        return Response({"detail": "Cart not found"}, status=404)

    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(["POST"])
def my_cart_items(request):
    user_id = request.data.get("user_id")
    if not user_id:
        return Response({"error": "Missing user_id"}, status=400)

    cart, _ = Cart.objects.get_or_create(customer_id=user_id)
    data = request.data.copy()
    data["cart"] = cart.pk

    serializer = CartItemSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
