import jwt
from django.http import JsonResponse
from rest_framework import status
from .config.env_config import ENV_VARIABLES
from ..users.models import User


class VerifyToken:
    def __init__(self, get_response):
        self.get_response = get_response

        def __call__(self, request):
            token = request.COOKIES.get("access_token")

            if not token:
                return JsonResponse(
                    {"message": "Invalid Token"}, status=status.HTTP_401_UNAUTHORIZED
                )

            try:
                payload = jwt.decode(
                    token, ENV_VARIABLES["ACCESS_TOKEN_SECRET"], algorithms=["HS256"]
                )

                user = User.objects.get(id=payload["id"])
                if not user:
                    return JsonResponse(
                        {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
                    )

                request.user = user
            except jwt.ExpiredSignatureError:
                return JsonResponse(
                    {"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED
                )
            except jwt.InvalidTokenError:
                return JsonResponse({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return JsonResponse({"error": "User not found"}, status=status.HTTP_401_UNAUTHORIZED)
            return self.get_response(request)

