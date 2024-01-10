from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from eventageousapi.models import Payment_Type

class Payment_TypeView(ViewSet):
  """views for payment"""
  def list(self, request):
    payment_types = Payment_Type.objects.all()
    serializer = Payment_TypeSerializer(payment_types, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class Payment_TypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Payment_Type
    fields = ('id', 'name')