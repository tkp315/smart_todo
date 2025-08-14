
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .serializers import UserSerializer
from rest_framework.response import Response
from .models import User
import jwt
import datetime
from core.config.env_config import ENV_VARIABLES

from .helpers import generate_token


@api_view(["POST"])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "User registered successfully"}, status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    try:
        user = User.objects.get(email=email)

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

    if not check_password(password, user.password):
        return Response(
            {"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST
        )

    access_token = generate_token(False, user)
    refresh_token = generate_token(True, user)

    res = Response({"message": "Logged In Successfully"}, status=status.HTTP_200_OK)

    res.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False if ENV_VARIABLES["DJANGO_ENV"] == "dev" else True,
        # samesite='',
        expires=datetime.datetime.utcnow()
        + datetime.timedelta(hours=ENV_VARIABLES["ACCESS_TOKEN_EXPIRY"]),
    )
    res.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False if ENV_VARIABLES["DJANGO_ENV"] == "dev" else True,
        # samesite='',
        expires=datetime.datetime.utcnow()
        + datetime.timedelta(hours=ENV_VARIABLES["REFRESH_TOKEN_EXPIRY"]),
    )
    return res


@api_view(["POST"])
def logout(request):
    res = Response({"message": "Logout Successfully"}, status=status.HTTP_200_OK)
    res.delete_cookie("access_token")
    res.delete_cookie("refresh_token")

    return res


@api_view(["POST"])
def refresh_token(request):
    refresh_token = request.COOKIES.get("refresh_token")

    if not refresh_token:
        return Response(
            {"message": "Refresh token not found"}, status=status.HTTP_400_BAD_REQUEST
        )
    try:
        decoded_token = jwt.decode(
            refresh_token, ENV_VARIABLES["REFRESH_TOKEN_SECRET"], algorithms=["HS256"]
        )

        if not decoded_token:
            return Response(
                {"message": "Invalid Refresh Token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        user = User.objects.get(id=decoded_token["id"])

        access_token = generate_token(False, user)

        res = Response({"message": "Logged In Successfully"}, status=status.HTTP_200_OK)
        res.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False if ENV_VARIABLES["DJANGO_ENV"] == "dev" else True,
            # samesite='',
            expires=datetime.datetime.utcnow()
            + datetime.timedelta(hours=ENV_VARIABLES["ACCESS_TOKEN_EXPIRY"]),
        )
        return res
    except jwt.ExpiredSignatureError:
        return Response(
            {"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED
        )
    except jwt.InvalidTokenError:
        return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response(
            {"error": "User not found"}, status=status.HTTP_401_UNAUTHORIZED
        )

@api_view(['GET'])
def user(request):
    user = request.user

    user_data = User.objects.get(id=user.id)

    if not user_data:
        Response({"error":"User not found"},status=status.HTTP_400_BAD_REQUEST)

    Response({"message":"User not found","result":user_data},status=status.HTTP_200_OK)