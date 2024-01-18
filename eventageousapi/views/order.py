from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from eventageousapi.models import Order, Ticket, Order_Ticket, Event, User, Payment_Type
from django.db.models import Q
from .user import UserSerializer
from .ticket import TicketSerializer

class OrderView(ViewSet):
  """views for order"""
  def retrieve(self, request, pk):
    order = Order.objects.get(pk=pk)
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def list(self, request):
    orders = Order.objects.all()
    
    customer = request.query_params.get('customerId', None)
    
    if request.query_params.get('completed', None) is not None and customer is not None:
      orders = orders.filter(completed = True, customer_id = customer)
    
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def update(self, request, pk):
    order = Order.objects.get(pk=pk)
    
    if 'paymentType' in request.data:
      payment_type = Payment_Type.objects.get(id=request.data['paymentType'])
      order.payment_type = payment_type
    
    if 'total' in request.data:  
      order.total = request.data['total']
      
    if 'billingAddress' in request.data:
      order.billing_address = request.data['billingAddress']
    
    if 'dateCompleted' in request.data:
      order.date_completed = request.data['dateCompleted']
    
    if 'completed' in request.data:
      order.completed = request.data['completed']
    
    order.save()
          
    serializer = OrderSerializer(order)
    
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  @action(methods=['get'], detail=True)
  def order_ticket_events(self, request, pk):
    order = Order.objects.get(pk=pk)
    order_tickets = [order_ticket.ticket for order_ticket in order.order_tickets.all()]
    discrete_event_tickets = []
    for ticket in order_tickets:
      if ticket not in discrete_event_tickets:
        discrete_event_tickets.append(ticket)
    serializer = TicketSerializer(discrete_event_tickets, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  @action(methods=['put'], detail=True)
  def add_ticket(self, request, pk):
    customer = User.objects.get(id=request.data['userId'])
    ticket = Ticket.objects.get(id=request.data['ticketId'])
    order = ''
    order_query = Order.objects.filter(Q(customer=customer) & Q(completed=False))
    if order_query.exists():
      assert len(order_query) == 1
      if len(order_query) == 1:
        order = list(order_query)[0]
    else:
      order = Order.objects.create(
        customer = customer,
      )
      
    event = Event.objects.get(id=request.data['eventId'])
    ticket = Ticket.objects.get(event=event)
    tickets_to_create = request.query_params.get('multiple', None)
    
    if tickets_to_create is None:
      Order_Ticket.objects.create(
        order = order,
        ticket = ticket
      )
    else:
      existing_order_tickets = Order_Ticket.objects.all().filter(order=order)
      for order_ticket in existing_order_tickets:
        order_ticket.delete()
        
      created_count = 0
      while created_count < int(tickets_to_create):
        Order_Ticket.objects.create(
        order = order,
        ticket = ticket
        )
        created_count += 1
        
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  @action(methods=['put'], detail=True)
  def remove_ticket(self, request, pk):
    customer = User.objects.get(id=request.data['userId'])
    ticket = Ticket.objects.get(event=request.data['ticketId'])
    order = ''
    order_query = Order.objects.filter(Q(customer=customer) & Q(completed=False))
    if order_query.exists():
      assert len(order_query) == 1
      if len(order_query) == 1:
        order = list(order_query)[0]
    else:
      order = Order.objects.create(
        customer = customer,
      )
        
    order_tickets = Order_Ticket.objects.all().filter(order=order, ticket=ticket)
    order_tickets_list = [order_ticket for order_ticket in order_tickets]
    if request.query_params.get('all') == 'True':
      for order_ticket in order_tickets_list:
        order_ticket.delete()
        
    else:
      delete_count = 0
      while delete_count < 0:
        for order_ticket in order_tickets:
          order_ticket.delete()
          delete_count += 1
    
    # delete all in case of errors
    # Order_Ticket.objects.all().delete()
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
    
    
class EventSerializer(serializers.ModelSerializer):
  seller = UserSerializer(many=False)
  class Meta:
    model = Event
    fields = ('id', 'name', 'description', 'tickets_available', 'date', 'image_url', 'seller')

class TicketSerializer(serializers.ModelSerializer):
  event = EventSerializer(many=False)
  class Meta:
    model = Ticket
    fields = ('id', 'event', 'price')  

class OrderSerializer(serializers.ModelSerializer):
  customer = UserSerializer()
  tickets = serializers.SerializerMethodField(allow_null=True)
  class Meta:
    model = Order
    fields = ('id', 'customer', 'payment_type', 'total',  'date_completed', 'completed', 'billing_address', 'tickets')
    
  def get_tickets(self, obj):
    order_tickets = Order_Ticket.objects.all().filter(order=obj)
    tickets_list = [order_ticket.ticket for order_ticket in order_tickets]
    serializer = TicketSerializer(tickets_list, many=True)
    if len(tickets_list) > 0:
      return serializer.data
    else:
      return []