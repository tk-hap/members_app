from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


def index_navigator(request):
    return render(request, "index_navigator.xml", {})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def home(request):
    return render(request, "home.xml", {})
