from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


def index(request):
    return render(request, "index.xml", {})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def home(request):
    return render(request, "home.xml", {})
