from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Trainer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    picture = models.ImageField(upload_to="trainers/")
    picture_thumbnail = ImageSpecField(
        source="picture",
        processors=[ResizeToFill(248, 248, anchor=(0, 0))],
        format="JPEG",
        options={"quality": 100},
    )
    bio = models.TextField()
    qualifications = models.TextField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
