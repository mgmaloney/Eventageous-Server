from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from eventageousapi.models import Event, User, Ticket

class EventView(ViewSet):
  """"views for events"""
  def retrieve(self, request, pk):
    event = Event.objects.get(pk=pk)
    serializer = EventSerializer(event)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def list(self, request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def create(self, request):
    seller = User.objects.get(id=request.data['sellerId'])
    event = Event.objects.create(
      name = request.data['name'],
      description = request.data['description'],
      tickets_available  = request.data['ticketsAvailable'],
      date = request.data['date'],
      image_url = request.data['imageUrl'],
      seller = seller    
    )
    Ticket.objects.create(
      event = event,
      price = request.data['ticketPrice']
    )
    serializer = EventSerializer(event)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  def update(self, request, pk):
    seller = User.objects.get(id=request.data['sellerId'])
    event = Event.objects.get(pk=pk)
    
    event.name = request.data['name'],
    event.description = request.data['description'],
    event.tickets_available  = request.data['ticketsAvailable'],
    event.date = request.data['date'],
    event.image_url = request.data['imageUrl'],
    event.seller = seller
    
    event.save()
    
    ticket = Ticket.objects.get(event=event)
    ticket.price = request.data['price']
    ticket.save()
   
    serializer = EventSerializer(event)
    
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def destroy(self, request, pk):
    event = Event.objects.get(pk=pk)
    event.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
      

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'uid', 'first_name', 'last_name', 'bio', 'email', 'address', 'phone_number', 'is_seller')

class TicketSerializer(serializers.ModelSerializer):
  class Meta:
    model = Ticket
    fields = ('price', )

class EventSerializer(serializers.ModelSerializer):
  seller = UserSerializer()
  ticket = serializers.SerializerMethodField()
  class Meta:
    model = Event
    fields = ('id', 'name', 'description', 'date', 'tickets_available', 'image_url', 'seller', 'ticket')
    
  def get_ticket(self, obj):
    ticket = Ticket.objects.get(event=obj)
    serializer = TicketSerializer(ticket)
    return serializer.data
      