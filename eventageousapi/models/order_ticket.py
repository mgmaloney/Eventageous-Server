from django.db import models
from .order import Order
from .ticket import Ticket

class Order_Ticket(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE)
  ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)