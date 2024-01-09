from django.db import models

class Payment_Type(models.Model):
  name = models.CharField(max_length=100, default='')