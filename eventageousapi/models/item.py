from django.db import models
from .user import User
from .category import Category

class Item(models.Model):
  name = models.CharField(max_length=200, default='')
  price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
  available_quantity = models.IntegerField(default=0)
  image_url = models.CharField(max_length=500, default='')
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  seller = models.ForeignKey(User, on_delete=models.CASCADE)