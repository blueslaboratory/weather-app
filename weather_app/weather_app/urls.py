from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('weather/', views.weather_view, name='weather'),
    path('weather/<str:city>/', views.weather_view, name='weather_city'),
]

