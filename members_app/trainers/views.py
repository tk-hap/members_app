from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .models import Trainer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def trainer_home(request):
    featured_trainers = Trainer.objects.filter(featured=True).order_by("first_name")
    return render(request, "trainers/trainer_home.xml", {"trainers": featured_trainers})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def trainer(request, trainer_id):
    trainer = Trainer.objects.get(id=trainer_id)
    return render(request, "trainers/trainer.xml", {"trainer": trainer})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def trainer_full_bio(request, trainer_id):
    trainer = Trainer.objects.get(id=trainer_id)
    return render(request, "trainers/full_bio.xml", {"trainer": trainer})