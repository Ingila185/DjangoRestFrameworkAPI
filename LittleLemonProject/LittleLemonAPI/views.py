from django.shortcuts import render
from .models import Cart, Category, MenuItems, Order, OrderItem, User
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_400_BAD_REQUEST
from .serializer import MenuItemSerializer, UserSerializer, CartSerializer, OrderSerializer
from django.contrib.auth.models import User, Group
# Create your views here.
@api_view(['GET', 'POST', 'PUT', 'PATCH','DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle, UserRateThrottle])

def menu(request):
    
    item_price = request.query_params.get('item_price')
    item_title = request.query_params.get('item_title')
    ordering = request.query_params.get('ordering')
    perpage = request.query_params.get('perpage', default = 2)
    page = request.query_params.get('page' , default = 1)

    if request.method == 'GET':
        if request.user.groups.filter(name__in =  ['Delivery Crew', 'Manager', 'Customer']):
                data = MenuItems.objects.all()
        if item_price:
            data = data.filter(price__lte = item_price)
        if item_title:
                data = data.filter(title__icontains = item_title)

        if ordering:
                data = data.order_by(ordering)    

        paginator = Paginator(data, per_page = perpage )
        try:
                data = paginator.page(number = page)
        except EmptyPage:
                data = []
        serialized_data = MenuItemSerializer(data, many = True)
        return Response(serialized_data.data, HTTP_200_OK)
    
    if request.method == 'POST':
        if request.user.groups.filter(name = 'Manager'):
            serialized_data = MenuItemSerializer(data = request.data)
            serialized_data.is_valid(raise_exception = True)
            serialized_data.save()
            return Response(serialized_data.data, HTTP_201_CREATED)
        else:
            return Response({"message":"Forbidden"} , HTTP_403_FORBIDDEN)        

    if request.method == 'PUT' or request.method == 'PATCH' or request.method == 'DELETE':
            return Response({"message":"Forbidden"} , HTTP_403_FORBIDDEN)        
        
    else:
            return Response({"message":"Forbidden"}, HTTP_403_FORBIDDEN)
    
      

@api_view(['GET', 'PUT', 'PATCH' , 'DELETE'])
@permission_classes([IsAuthenticated])
def menu_item(request, id):

    if request.method=='GET':
        if request.user.groups.filter(name__in = ['Manager', 'Delivery Crew','Customer']):
            
            data = get_object_or_404(MenuItems, pk = id)
            serialized_data = MenuItemSerializer(data)
            return Response(serialized_data.data)
        else:
            return Response({"message":"Forbidden"}, HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
       
       if request.user.groups.filter(name = 'Manager'):
            item = get_object_or_404(MenuItems, pk = id)
            serialized_data = MenuItemSerializer(item, data = request.data)
            serialized_data.is_valid(raise_exception = True)
            serialized_data.save()
            return Response(serialized_data.data, HTTP_200_OK)
           

       else:      
            return Response({"message":"Forbidden"}, HTTP_403_FORBIDDEN)

    if request.method == 'PATCH':
        if request.user.groups.filter(name = 'Manager'):
            item = get_object_or_404(MenuItems, pk = id)
            serialized_data = MenuItemSerializer(item, data = request.data)
            serialized_data.is_valid(raise_exception = True)
            serialized_data.save()
            return Response(serialized_data.data, HTTP_200_OK)
           
        else:
            return Response({"message":"Forbidden"}, HTTP_403_FORBIDDEN)

    if request.method == 'DELETE':
        if request.user.groups.filter(name = 'Manager'):
            item = get_object_or_404(MenuItems, pk = id)
            data = item.delete()
            return Response({"message": data}, HTTP_200_OK)
           
        else:
            return Response({"message":"Forbidden"}, HTTP_403_FORBIDDEN) 
         
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def manager(request):
    if request.user.groups.filter(name = 'Manager'):

        if request.method == 'POST':
        
            username = request.data['username']
            if username:
                user = get_object_or_404(User, username = username)
                managers = Group.objects.get(name = "Manager")
                managers.user_set.add(user)
                return Response({"message":"User assigned to Manager successfully."}, HTTP_201_CREATED)
        
        if request.method == 'DELETE':
                username = request.data['username']
                managers.user_set.remove(user)
                return Response({"message":"ok"}, HTTP_200_OK)    
        
        if request.method == 'GET':
                managers = User.objects.filter(groups__name = 'Manager')
                serialized_managers = UserSerializer(managers, many = True)
                return Response(serialized_managers.data, HTTP_200_OK)    

        
        return Response({"Message":"Error"}, HTTP_400_BAD_REQUEST)
    else:
        return Response({"message":"Forbidden"}, HTTP_403_FORBIDDEN)

@api_view(['GET','DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def manager_id(request, id):

    user = get_object_or_404(User, username = id)

    # if request.method == 'POST':
        
    #         username = request.data['username']
    #         if username:
    #             user = get_object_or_404(User, username = username)
    #             manager = Group.objects.get(name = "Manager")
    #             manager.user_set.add(user)
    #             manager.save()
    #             return Response({"message":"OK"}, HTTP_201_CREATED)
        
    if request.method == 'GET':
              #GET user details or throw 404
               serializedUser = UserSerializer(user)
               return Response(serializedUser.data, HTTP_200_OK)

    if request.method == 'DELETE':
         #Delete user from group
                group = Group.objects.get(name='Manager') 
                user.groups.remove(group)
                user.save()
                return Response({"message":"User removed successfully"}, HTTP_200_OK)
    
    return Response({"message":"Forbidden"}, HTTP_403_FORBIDDEN)


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def deliveryCrew(request):
    if request.user.groups.filter(name = 'Manager'):

        if request.method == 'POST':
        
            username = request.data['username']
            if username:
                user = get_object_or_404(User, username = username)
                crew = Group.objects.get(name = "Delivery Crew")
                crew.user_set.add(user)
                crew.save()
                return Response({"message":"User Assigned to Delivery Crew successfully."}, HTTP_201_CREATED)
        
        
          
        if request.method == 'GET':
                deliveryCrew = User.objects.filter(groups__name = 'Delivery Crew')
                serialized_deliveryCrew = UserSerializer(deliveryCrew, many = True)
                return Response(serialized_deliveryCrew.data, HTTP_200_OK)    
    
        return Response({"Message":"Error"}, HTTP_400_BAD_REQUEST)
    else:
        return Response({"message":"Forbidden"}, HTTP_403_FORBIDDEN)

@api_view(['GET','DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def deliveryCrew_id(request, id):
    user = get_object_or_404(User, username = id)

    if request.user.groups.filter(name = 'Manager'):
         
         if request.method == 'GET':
              #GET user details or throw 404
               serializedUser = UserSerializer(user)
               return Response(serializedUser.data, HTTP_200_OK)


         if request.method == 'DELETE':
              #remove the user<id>  from delivery crew group
                group = Group.objects.get(name='Delivery Crew') 
                user.groups.remove(group)
                user.save()
                return Response({"message":"User removed successfully"}, HTTP_200_OK)
   
              

    else:
                   
        return Response({"message":"Forbidden"}, HTTP_403_FORBIDDEN)


@api_view(['GET', 'POST','DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle, UserRateThrottle])

def order(request):
   
    ordering = request.query_params.get('ordering')
    perpage = request.query_params.get('perpage', default = 2)
    page = request.query_params.get('page' , default = 1)

    orders = Order.objects.all()

    if ordering:
            orders = orders.order_by(ordering)    

    paginator = Paginator(orders, per_page = perpage )
    try:
        orders = paginator.page(number = page)
    except EmptyPage:
            orders = []

    if request.user.groups.filter(name__in = ['Manager', 'Delivery Crew', 'Customer']):
        if request.method == 'GET':
            serialized_orders = OrderSerializer(orders, many = True)
            return Response(serialized_orders.data, HTTP_200_OK)
             
        
    if request.method == 'POST':
            if request.user.groups.filter(name__in = ['Manager', 'Delivery Crew', 'Customer']):
                serialized_data = OrderSerializer(data = request.data)
                serialized_data.is_valid(raise_exception = True)
                serialized_data.save()
                return Response(serialized_data.data, HTTP_201_CREATED)

    if request.method == 'DELETE':
            if request.user.groups.filter(name = 'Manager'):
                order = get_object_or_404(Order, pk = id)
                data = order.delete()
                return Response({"message": data}, HTTP_200_OK)
    else:
        return Response({"message":"Forbidden"}, HTTP_403_FORBIDDEN)



      

@api_view(['GET', 'PUT','PATCH', 'DELETE'])
def order_id(request, id):
    if request.user.groups.filter(name__in = ['Manager', 'Delivery Crew', 'Customer']):
        if request.method == 'GET':
            data = get_object_or_404(Order, pk = id)
            serialized_data = OrderSerializer(data)
            return Response(serialized_data.data)
        if request.method == 'POST':
            serialized_data = OrderSerializer(data = request.data)
            serialized_data.is_valid(raise_exception = True)
            serialized_data.save()
            return Response(serialized_data.data, HTTP_201_CREATED)
        
        if request.method == 'PUT' or request.method == 'PATCH':
            item = get_object_or_404(Order, pk = id)
            serialized_data = OrderSerializer(item, data = request.data)
            serialized_data.is_valid(raise_exception = True)
            serialized_data.save()
            return Response(serialized_data.data, HTTP_201_CREATED)

        if request.method == 'DELETE':
            item = get_object_or_404(Order, pk = id)
            deleted = item.delete()
            return Response({"message": str(deleted[0]) + str(" rows deleted")}, HTTP_200_OK)
               
    else:
        return Response({"message":"Forbidden"}, HTTP_403_FORBIDDEN)

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def cart(request):
    if request.user.groups.filter(name = 'Customer'):
        if request.method == 'GET':
            data = Cart.objects.all()
            serialized_data = CartSerializer(data, many = True)
            return Response(serialized_data.data, HTTP_200_OK)
        
        if request.method == 'POST':
            serialized_data = CartSerializer(data = request.data)
            serialized_data.is_valid(raise_exception = True)
            serialized_data.save()
            return Response(serialized_data.data, HTTP_201_CREATED)

        if request.method == 'DELETE':
            deleted = Cart.objects.all().delete()
            return Response({"message": str(deleted[0]) + str(" rows deleted")}, HTTP_200_OK)
               
    
    else:
        return Response({"message": "Forbidden"}, HTTP_403_FORBIDDEN)
