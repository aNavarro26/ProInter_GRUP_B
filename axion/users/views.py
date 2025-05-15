from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response

from rest_framework import status
from .models import User
from .serializer import UserSerializer
from django.contrib.auth.hashers import check_password, make_password


@api_view(["GET", "PUT", "DELETE"])
def user_detail(request, user_id):
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == "PUT":
        password = request.data.get("password")
        if not password:
            return Response(
                {"error": "Password is required for verification"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not check_password(password, user.password):
            return Response(
                {"error": "Incorrect password"}, status=status.HTTP_403_FORBIDDEN
            )

        update_data = request.data.copy()

        if "new_password" in update_data:
            update_data["password"] = update_data.pop("new_password")

        serializer = UserSerializer(user, data=update_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        user.delete()
        return Response(
            {"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Username and password required"}, status=400)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=401)

    if not check_password(password, user.password):
        return Response({"error": "Invalid credentials"}, status=401)

    request.session["user_id"] = user.user_id
    return Response({"message": "Login successful", "user_id": user.user_id})


@api_view(["POST"])
@permission_classes([AllowAny])
def signup_view(request):
    username = request.data.get("username")
    full_name = request.data.get("full_name")
    email = request.data.get("email")
    password = request.data.get("password")
    confirm_password = request.data.get("confirm_password")
    address = request.data.get("address", "")

    # Validaciones básicas
    if not all([username, full_name, email, password, confirm_password]):
        return Response(
            {"error": "Todos los campos (excepto address) son obligatorios."},
            status=400,
        )
    if password != confirm_password:
        return Response({"error": "Las contraseñas deben coincidir."}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({"error": "El nombre de usuario ya está en uso."}, status=400)
    if User.objects.filter(email=email).exists():
        return Response(
            {"error": "El correo electrónico ya está registrado."}, status=400
        )

    # Crear el usuario con role="Customer"
    customer = User.objects.create(
        username=username,
        full_name=full_name,
        email=email,
        password=make_password(password),
        address=address,
        role="Customer",
    )

    return Response(
        {"message": "Usuario creado con éxito.", "user_id": customer.user_id},
        status=201,
    )
