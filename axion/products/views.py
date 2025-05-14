from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
import os
from .models import Product
from .serializers import ProductSerializer


@api_view(["GET", "POST"])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def product_list_create(request):
    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(
            products, many=True, context={"request": request}
        )
        return Response(serializer.data)

    # POST con JSON o multipart
    data = request.data.copy()
    images = request.FILES.getlist("images")

    serializer = ProductSerializer(data=data, context={"request": request})
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    product = serializer.save()

    if images:
        paths = []
        for idx, img in enumerate(images, start=1):
            ext = os.path.splitext(img.name)[1] or ".jpg"
            filename = f"products/{product.product_id}-{idx}{ext}"
            default_storage.save(filename, img)
            paths.append(filename)
        product.image_url = ",".join(paths)
        product.save()

    out = ProductSerializer(product, context={"request": request})
    return Response(out.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def product_detail(request, product_id):
    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        return Response(
            {"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = ProductSerializer(product, context={"request": request})
        return Response(serializer.data)

    elif request.method == "PUT":
        data = request.data.copy()
        images = request.FILES.getlist("images")

        serializer = ProductSerializer(product, data=data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product = serializer.save()

        if images:
            paths = []
            for idx, img in enumerate(images, start=1):
                ext = os.path.splitext(img.name)[1] or ".jpg"
                filename = f"products/{product.product_id}-{idx}{ext}"
                default_storage.save(filename, img)
                paths.append(filename)
            product.image_url = ",".join(paths)
            product.save()

        out = ProductSerializer(product, context={"request": request})
        return Response(out.data)

    else:
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
