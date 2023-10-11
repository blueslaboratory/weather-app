"""
URL configuration for weather_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    # http://127.0.0.1:8000/
    path('', views.weather_view, name='weather'),
    path('admin/', admin.site.urls),
    # http://127.0.0.1:8000/weather/
    path('weather/', views.weather_view, name='weather'),
    # http://127.0.0.1:8000/weather/Madrid/
    path('weather/<str:city>/', views.weather_view, name='weather_city'),

    # http://127.0.0.1:8000/weather/saved
    path('weather/saved', views.saved_cities, name='saved_cities'),
    # http://127.0.0.1:8000/weather/saved/Madrid
    path('weather/saved/<str:city>/', views.get_weather_by_city, name='get_weather_by_city'),

    # http://127.0.0.1:8000/weather/delete_data
    # path('weather/delete_data', views.delete_data, name='delete_data'),
]

