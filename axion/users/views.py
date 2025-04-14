from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer
from django.contrib.auth.hashers import check_password, make_password


@api_view(["GET", "PUT", "DELETE"])
def user_detail(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
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

        new_password = update_data.get("new_password")
        if new_password:
            update_data["password"] = make_password(new_password)

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
