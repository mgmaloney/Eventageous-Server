from django.db import models
from .order import Order
from .ticket import Ticket

class Order_Ticket(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_tickets')
  ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='ticket_orders')