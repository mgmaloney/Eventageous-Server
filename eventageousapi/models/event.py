from django.db import models
from .user import User

class Event(models.Model):
  name = models.CharField(max_length=200, default='')
  description = models.CharField(max_length=500, default='')
  date = models.CharField(max_length=26, blank=True, null=True)
  tickets_available = models.PositiveIntegerField(default=0)
  image_url = models.CharField(max_length=500, default='')
  seller = models.ForeignKey(User, on_delete=models.CASCADE)