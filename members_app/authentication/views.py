from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from users.models import User 


@csrf_exempt
def login(request):
    if request.method == "GET":
        return render(request, "authentication/login.xml", {})

    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            return status.HTTP_400_BAD_REQUEST  # TODO: error response

        if User.objects.filter(username=username).exists():
            user = authenticate(None, username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                response = render(request, "authentication/redirect.xml", {})
                response["Auth-Token"] = token
                return response

            else:
                return  # TODO: error response