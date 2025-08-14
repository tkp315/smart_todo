from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Daily_Context
from core.config.env_config import ENV_VARIABLES

import json
import datetime

# Create your views here.

@api_view(['POST'])
def add_context(request):
    payload = request.data['payload']
    user = request.user
    is_dummy = request.is_dummy
    specific_user = True if is_dummy == False else False

    if not payload:
        return Response({'error':"Required fields are missing"},status=status.HTTP_400_BAD_REQUEST)

    if payload['content']:
         return  Response({'error':"Required fields are missing"},status=status.HTTP_400_BAD_REQUEST)

    context = Daily_Context.objects.create(
         source_type= payload.get('source_type',None),
         content= payload['content'],
         content_type = payload.get('content_type'),
         time = datetime.datetime.now(),
         user_id= user.id if specific_user==True else None
    )

    return Response({"message":"Daily context added successfully"},status=status.HTTP_201_CREATED)


@api_view(["GET"])
def daily_contexts(request):
    user = request.user
    is_dummy = request.is_dummy

    specific_user = True if is_dummy == False else False

    data = (
        Daily_Context.objects.filter().order_by("-created_at")
        if specific_user == False
        else Daily_Context.objects.filter(user_id=user.id).order_by("-created_at")
    )

    print("daily context data", data)

    if not data or len(data) == 0:
        Response(
            {"message": "No daily context data found"}, status=status.HTTP_204_NO_CONTENT
        )

    # need to check once
    Response(
        {"message": "Successfully created daily context", "result": data},
        status=status.HTTP_200_OK,
    )

    


    
