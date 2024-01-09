from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import Item, User, Category
from .category import CategorySerializer

class ItemView(ViewSet):
  """views for item"""
  def retrieve(self, request, pk):
    item = Item.objects.get(pk=pk)
    serializer = ItemSerializer(item, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def list(self, request):
    items = Item.objects.all()
    
    seller = request.query_params.get('sellerId', None)
    category = request.query_params.get('categoryId', None)
    
    if seller is not None:
      items = items.filter(seller_id = seller)
    
    if category is not None:
      items = items.filter(category_id = category)
    
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def create(self, request):
    seller = User.objects.get(id=request.data['sellerId'])
    category = Category.objects.get(id=request.data['categoryId'])
    item = Item.objects.create(
      name = request.data['name'],
      price = request.data['price'],
      available_quantity = request.data['availableQuantity'],
      image_url = request.data['imageUrl'],
      category = category,
      seller = seller
    )
    serializer = ItemSerializer(item, many=False)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  def update(self, request, pk):
    seller = User.objects.get(id=request.data['sellerId'])
    category = Category.objects.get(id=request.data['categoryId'])
    item = Item.objects.get(pk=pk)
    
    item.name = request.data['name']
    item.price = request.data['price']
    item.available_quantity = request.data['availableQuantity']
    item.image_url = request.data['imageUrl']
    item.category = category
    item.seller = seller
    
    item.save()
    
    serializer = ItemSerializer(item, many=False)
    
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def destroy(self, request, pk):
    item = Item.objects.get(pk=pk)
    item.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'uid', 'first_name', 'last_name', 'bio', 'email', 'address', 'phone_number', 'is_seller')

class ItemSerializer(serializers.ModelSerializer):
  category = CategorySerializer(many=False)
  seller = UserSerializer(many=False)
  class Meta:
    model = Item
    fields = ('id', 'name', 'price', 'available_quantity', 'image_url', 'category', 'seller')