from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.db.models import Q
from eventageousapi.models import User, Order, Order_Ticket
from .ticket import TicketSerializer

class UserView(ViewSet):
  @action(methods=['POST'], detail=True)
  def has_order(self, request, pk):
    customer = User.objects.get(pk=pk)
    order_query = Order.objects.filter(Q(customer=customer) & Q(completed=False))
    if order_query.exists():
      if len(order_query) == 1:
        order = list(order_query)[0]
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
      else:
        new_order = Order.objects.create(
          customer = customer,
        )
        serializer = OrderSerializer(new_order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    



class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'uid', 'first_name', 'last_name', 'bio', 'email', 'address', 'phone_number', 'is_seller')

class OrderSerializer(serializers.ModelSerializer):
  customer = UserSerializer()
  tickets = serializers.SerializerMethodField(allow_null=True)
  class Meta:
    model = Order
    fields = ('id', 'customer', 'payment_type', 'total', 'billing_address', 'date_completed', 'completed', 'tickets')
    
  def get_tickets(self, obj):
    order_tickets = Order_Ticket.objects.all().filter(order=obj)
    tickets_list = [order_ticket.ticket for order_ticket in order_tickets]
    serializer = TicketSerializer(tickets_list, many=True)
    if len(tickets_list) > 0:
      return serializer.data
    else:
      return []