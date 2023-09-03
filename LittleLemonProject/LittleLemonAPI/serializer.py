from rest_framework import serializers
from .models import Cart, Category, MenuItems, Order, OrderItem, User

class MenuItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuItems
        fields = ['id', 'title', 'price', 'featured' , 'category']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model= User
        fields = ['username','email', 'is_staff']

class CartSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= Cart
        fields = ['user', 'menuitem', 'quantity', 'unit_price','price']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user' , 'delivery_crew' , 'status', 'total' , 'date' ]