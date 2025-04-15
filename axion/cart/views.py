from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from .serializer import CartSerializer, CartItemSerializer


@api_view(["GET", "POST"])
def cart_list_create(request):
    if request.method == "GET":
        carts = Cart.objects.all()
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)

    serializer = CartSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def cart_detail(request, cart_id):
    try:
        cart = Cart.objects.get(pk=cart_id)
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
        cart = Cart.objects.get(pk=cart_id)
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
    try:
        cart = Cart.objects.get(pk=cart_id)
    except Cart.DoesNotExist:
        return Response({"detail": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        item = cart.items.get(pk=cart_item_id)
    except CartItem.DoesNotExist:
        return Response(
            {"detail": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND
        )

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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
