from django.contrib import admin
from django.urls import path, include
from LittleLemonAPI import views


urlpatterns = [
path('menu-items', views.menu, name = "menu" ),
path('menu-items/<int:id>', views.menu_item, name = "menu" ),
#path('users', views.users),
#path('users/<int:id>', views.users),
#path('auth/', include('rest_framework.urls') ) //if user auth is done by DRF
path('auth/', include('djoser.urls')),
path('auth/', include('djoser.urls.authtoken')),
path('groups/manager/users',views.manager),
path('groups/delivery-crew/users',views.deliveryCrew),
path('groups/delivery-crew/users/<str:id>',views.deliveryCrew_id),

path('groups/manager/users/<str:id>',views.manager_id),
path('cart/menu-items', views.cart),
path('orders', views.order),
path('orders/<int:id>', views.order_id),

]