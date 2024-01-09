from django.db import models
from .order import Order
from .event import Item

class Order_Ticket(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE)
  ticket = models.ForeignKey(Item, on_delete=models.CASCADE)