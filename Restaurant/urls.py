#define URL route for index() view
from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter as router


urlpatterns = [

    path('', views.index, name='index'),
    path('api-auth/', include('djoser.urls')),
    path('api-auth/', include('djoser.urls.authtoken')),
    path('restapi-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('menu/', views.MenuItemsView.as_view()),
    path('menu/<int:pk>', views.SingleMenuItemView.as_view()),
    path('booking/', views.BookingViewSet.as_view({"get":"list"})),
    path('auth/', include('djoser.urls')),
    path('api-token-auth/', obtain_auth_token),
    path('auth/', include('djoser.urls.authtoken'))

    
]
