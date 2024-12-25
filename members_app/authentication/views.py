from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

@csrf_exempt
def login(request):
    if request.method == "GET":
        return render(request, "authentication/login.xml", {})

    if request.method != "POST":
        return render(request, "authentication/failure.xml", {})

    username = request.POST.get("username")
    password = request.POST.get("password")

    if not username or not password:
        return render(request, "authentication/failure.xml", {})

    user = authenticate(None, username=username, password=password)
    if user is None:
        return render(request, "authentication/failure.xml", {})

    token, created = Token.objects.get_or_create(user=user)
    response = render(request, "authentication/redirect.xml", {})
    response["Auth-Token"] = token
    return response