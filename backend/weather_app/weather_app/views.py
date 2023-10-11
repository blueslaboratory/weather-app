import requests
from django.http import JsonResponse

import datetime
import pycountry

# Esto no va, no consigo importar desde otro modulo
# from ..weather_db.views import guardar_datos_en_db
# from backend.weather_db.views import guardar_datos_en_db

from .functions import *
from .models import WeatherInfo

from django.db import connection


# Recuperar datos de la DB por ciudad
def get_weather_by_city(request, city_id):

    try:
        # Buscar registros en la base de datos que coincidan con la ciudad
        weather_data = WeatherInfo.objects.filter(id=city_id)

        if not weather_data:
            return JsonResponse({'error': 'No se encontraron datos para la ciudad especificada'}, status=404)

        # Convierte los datos en un diccionario
        weather_info = {}

        for record in weather_data:
            weather_info['country'] = record.country
            weather_info['city'] = record.city
            weather_info['longitude'] = record.longitude
            weather_info['latitude'] = record.latitude
            weather_info['temperature'] = record.temperature
            weather_info['feels_like'] = record.feels_like
            weather_info['temp_min'] = record.temp_min
            weather_info['temp_max'] = record.temp_max
            weather_info['humidity'] = record.humidity
            weather_info['sunrise'] = record.sunrise.strftime('%H:%M:%S')
            weather_info['sunset'] = record.sunset.strftime('%H:%M:%S')
            weather_info['description'] = record.description
            weather_info['api_url'] = record.api_url


        # Devuelve los datos como una respuesta JSON
        return JsonResponse(weather_info)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Guardar los datos de las ciudades dentro de la DB
def guardar_cities(request):
    delete_data(request)

    ciudades = {
        1: 'madrid',
        2: 'sevilla',
        3: 'barcelona',
        4: 'valencia',
        5: 'zaragoza',
        6: 'bilbao',
        7: 'vigo',
        8: 'cadiz',
        9: 'burgos',
        10: 'ibiza'
    }

    for c in ciudades.values():
        weather_view(request, c)

    return JsonResponse({'message': 'saved_cities correctly executed'})



# Borrar todos los contenidos de la tabla weather_app_weatherinfo
def delete_data(request):
    WeatherInfo.objects.all().delete()
    reset_sequence()
    return JsonResponse({'success': 'Datos eliminados correctamente'}, status=400)


# Resetear los ids
def reset_sequence():
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='weather_app_weatherinfo';")


# llamada a la api normal
def weather_view(request, city = None):
    # A no ser que me lo pases por URL,
    # obtén el parámetro 'city' de la solicitud GET
    if city == None:
        city = request.GET.get('city')

    # Reemplaza 'TU_API_KEY' con tu clave API de OpenWeatherMap
    api_key = '073d3b7b9dbd1aed508be40f3f703f98'

    # Realiza una solicitud a la API de OpenWeatherMap para obtener datos meteorológicos
    # Llamar a la API: https://openweathermap.org/current#name
    # https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}
    # https://api.openweathermap.org/data/2.5/weather?q=Madrid&appid=073d3b7b9dbd1aed508be40f3f703f98

    api_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(api_url)

    # Procesa la respuesta JSON de la API y extrae los datos necesarios
    if response.status_code == 200:
        weather_data = response.json()

        longitude = weather_data['coord']['lon']
        latitude = weather_data['coord']['lat']

        country = get_location_info(api_key, latitude, longitude)['country']
        city = get_location_info(api_key, latitude, longitude)['city']

        # city = weather_data['name']

        temperature = kelvin_to_celsius(weather_data['main']['temp'])
        feels_like = kelvin_to_celsius(weather_data['main']['feels_like'])
        temp_min = kelvin_to_celsius(weather_data['main']['temp_min'])
        temp_max = kelvin_to_celsius(weather_data['main']['temp_max'])

        humidity = weather_data['main']['humidity']

        sunrise = sun_formatter(weather_data['sys']['sunrise'])
        sunset = sun_formatter(weather_data['sys']['sunset'])

        weather_description = weather_data['weather'][0]['description']

        # Crea un diccionario con los datos meteorológicos
        weather_info = {
            # 'city': city,
            'location': {
                'country': country,
                'city': city,
            },
            'longitude': longitude,
            'latitude': latitude,
            'temperature': {
                'celsius': temperature,
                'feels_like': feels_like,
                'temp_min': temp_min,
                'temp_max': temp_max,
            },
            'humidity': humidity,
            'sun': {
                'sunrise': sunrise,
                'sunset': sunset
            },
            'description': weather_description,
            'api_url': api_url,
        }

        # Guardame los datos en la DB:
        saved = guardar_datos_en_db2(weather_info)
        weather_info['saved'] = saved

        # Devuelve una respuesta JSON con los datos
        return JsonResponse(weather_info)

    # En caso de error, devuelve una respuesta de error JSON
    return JsonResponse({
        'city': city,
        'error': 'No se pudo obtener la informacion meteorologica.'
    }, status=400)


def get_location_info(api_key, latitude, longitude):
    # Llama a la API de geocodificación inversa para obtener información sobre la ubicación
    api_url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}'
    response = requests.get(api_url)

    # condición que verifica si el código de estado de una respuesta HTTP es igual a 200.
    if response.status_code == 200:
        location_data = response.json()

        # Extrae el nombre de la ciudad y el país
        city = location_data['name']
        country_code = location_data['sys']['country']
        country = country_code_to_country(country_code)

        return {'city': city, 'country': country}
    else:
        return None



def kelvin_to_celsius(kelvin):
    return float(kelvin) - 273.15


def sun_formatter(sun_time):

    # Convertir a objetos de fecha y hora
    sun_datetime = datetime.datetime.utcfromtimestamp(sun_time)

    # Formatear como horas legibles
    sun_time_formatted = sun_datetime.strftime('%H:%M:%S')

    return sun_time_formatted


def country_code_to_country(country_code):
    country_name = pycountry.countries.get(alpha_2=country_code).name
    return country_name