from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User


# Django Rest Framework view that takes a post request including the Expo push token and adds it to the users model
@api_view(["POST"])
@parser_classes([JSONParser])
@permission_classes([IsAuthenticated])
def save_push_token(request):
    try:
        # Extract Expo push token from request data
        push_token = request.data.get("PushToken")

        if not push_token:
            return Response(
                {"error": "Expo push token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get the current authenticated user
        user = request.user

        # Save the Expo push token to the user's model
        user.push_token = push_token
        user.save()

        return Response(
            {"message": "Expo push token saved successfully"}, status=status.HTTP_200_OK
        )
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
