from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import date
from rest_framework import status
from .models import Order, OrderItem, Shipment, Payment
from .serializers import OrderSerializer, OrderItemSerializer, ShipmentSerializer


@api_view(["POST"])
def order_list(request):
    if request.method == "POST":
        data = request.data.copy()
        data["order_date"] = date.today()
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order).data, status=201)
        return Response(serializer.errors, status=400)


@api_view(["GET"])
def order_user_list(request, user_id):
    if request.method == "GET":
        orders = Order.objects.filter(customer=user_id)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


@api_view(["GET", "PUT", "DELETE"])
def order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def order_items_list(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return Response(
            {"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        items = order.items.all()
        serializer = OrderItemSerializer(items, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        data = request.data.copy()
        data["order"] = order_id
        serializer = OrderItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def order_item_detail(request, order_id, order_item_id):
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return Response(
            {"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND
        )

    try:
        item = order.items.get(pk=order_item_id)
    except OrderItem.DoesNotExist:
        return Response(
            {"detail": "OrderItem not found."}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = OrderItemSerializer(item)
        return Response(serializer.data)
    elif request.method == "PUT":
        data = request.data.copy()
        data["order"] = order_id
        serializer = OrderItemSerializer(item, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def shipment_list(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return Response(
            {"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        shipments = order.shipments.all()
        serializer = ShipmentSerializer(shipments, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        data = request.data.copy()
        data["order"] = order_id
        serializer = ShipmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def shipment_detail(request, order_id, shipment_id):
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return Response(
            {"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND
        )

    try:
        shipment = order.shipments.get(pk=shipment_id)
    except Shipment.DoesNotExist:
        return Response(
            {"detail": "Shipment not found."}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = ShipmentSerializer(shipment)
        return Response(serializer.data)
    elif request.method == "PUT":
        data = request.data.copy()
        data["order"] = order_id
        serializer = ShipmentSerializer(shipment, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        shipment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["PATCH"])
def update_order_status(request, order_id):
    try:
        order = Order.objects.get(pk=order_id, customer_id=request.data.get("customer"))
    except Order.DoesNotExist:
        return Response({"detail": "Order not found"}, status=404)

    new_status = request.data.get("status")
    if new_status not in dict(Order.STATUS_CHOICES):
        return Response({"error": "Invalid status"}, status=400)

    order.status = new_status
    order.save()
    serializer = OrderSerializer(order)
    return Response(serializer.data)


@api_view(["POST"])
def process_checkout(request):
    data = request.data.copy()
    data["order_date"] = date.today()
    data["status"] = "Completed"

    serializer = OrderSerializer(data=data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    order = serializer.save()

    Shipment.objects.create(order=order, shipment_date=date.today())

    payment = data.get("payment", {})
    Payment.objects.create(
        order=order,
        method=payment.get("method"),
        card_number=payment.get("card_number"),
        expiry_date=payment.get("expiry"),
        cvv=payment.get("cvv"),
    )

    return Response(
        {"message": "Pedido completado", "order_id": order.order_id},
        status=status.HTTP_201_CREATED,
    )
