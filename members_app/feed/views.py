from django.shortcuts import render
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import Notification

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def feed_home(request):
    context = {"next": 1}
    return render(request, "feed/feed.xml", context)
 

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def feed_page(request, page):
    notifications = Notification.objects.filter(recipient=request.user)
    paginator = Paginator(notifications, per_page=40)
    page_object = paginator.get_page(page)
    next_page = page + 1
    context = {"page": page_object, "next": next_page}

    return render(request, "feed/page.xml", context)