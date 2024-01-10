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
    return Response(serializer.data, many=True)

  def create(self, request):
    seller = User.object.get(id=request.data['sellerId'])
    event = Event.objects.create(
      name = request.data(['name']),
      description = request.data['description'],
      tickets_available  = request.data['ticketsAvailable'],
      date = request.data['date'],
      image_url = request.data['image_url'],
      seller = seller    
    )
    Ticket.objects.create(
      event = event,
      price = request.data['ticketPrice']
    )
    serializer = EventSerializer(event)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  def update(self, request, pk):
    seller = User.object.get(id=request.data['sellerId'])
    event = Event.objects.get(pk=pk)
    
    event.name = request.data(['name']),
    event.description = request.data['description'],
    event.tickets_available  = request.data['ticketsAvailable'],
    event.date = request.data['date'],
    event.image_url = request.data['image_url'],
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
      

class EventSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Event
    fields = ('id')