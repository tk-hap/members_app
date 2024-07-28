from django.contrib import admin
from .models import Member, ExerciseClass, Trainer

# Register your models here.
admin.site.register(Member)
admin.site.register(ExerciseClass)
admin.site.register(Trainer)
