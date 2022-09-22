from django.db import models
from django.utils import timezone

class Predictions(models.Model):
    predict_datetime = models.DateTimeField(default=timezone.now)
    lyrics = models.TextField(blank=True)
    lyrics_post = models.TextField(blank=True)
    summary = models.TextField(blank=True)