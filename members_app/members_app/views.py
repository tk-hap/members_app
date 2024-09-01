from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated 
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import api_view, authentication_classes


def index(request):
    return render(request, "index.xml", {})

# A view that loads when the React Native app first loads to check if the user is authenticated via the token
# If the user is authenticated, the user is redirected to the home page
# If the user is not authenticated, the user is redirected to the login page
def check_auth(request):
    if request.user:
        return render(request, "home.xml", {})


@api_view(["GET"])
@authentication_classes([])
def home(request):
    user = None
    try:
       auth_result = TokenAuthentication().authenticate(request)
       if auth_result is not None:
           user = auth_result[0]
    except AuthenticationFailed:
        return render(request, "authentication/login.xml", {})

    if user:
        return render(request, "home.xml", {})
    else:
        return render(request, "authentication/login.xml", {})