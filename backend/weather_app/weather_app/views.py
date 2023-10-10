import requests
from django.http import JsonResponse

import datetime
import pycountry

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
        location = get_location_info(api_key, latitude, longitude)

        city = weather_data['name']

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
            'location': location,
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
            'api_url': api_url
        }

        # Devuelve una respuesta JSON con los datos
        return JsonResponse(weather_info)

    # En caso de error, devuelve una respuesta de error JSON
    return JsonResponse({'error': 'No se pudo obtener la información meteorológica.'}, status=400)


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