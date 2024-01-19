from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from eventageousapi.models import User, Ticket, Event

class TicketView(ViewSet):
  """views for ticket"""
  def retrieve(self, request, pk):
    ticket = Ticket.objects.get(pk=pk)
    serializer = TicketSerializer(ticket, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def list(self, request):
    tickets = Ticket.objects.all()
    
    
    serializer = TicketSerializer(tickets, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def create(self, request):
    event = Event.objects.get(id=request.data['eventId'])
    ticket = Ticket.objects.create(
      price = request.data['price'],
      event = event
    )
    serializer = TicketSerializer(ticket, many=False)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  def update(self, request, pk):
    event = Event.objects.get(id=request.data['eventId'])
    ticket = Ticket.objects.get(pk=pk)
    
    ticket.event = event
    ticket.price = request.data['price']
    ticket.save()
    
    serializer = TicketSerializer(ticket, many=False)
    
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def destroy(self, request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  

    

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'uid', 'first_name', 'last_name', 'bio', 'email', 'address', 'phone_number', 'is_seller')

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