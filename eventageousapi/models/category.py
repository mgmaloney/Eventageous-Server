from django.db import models

class Category(models.Model):
  description = models.CharField(max_length=350, default='')