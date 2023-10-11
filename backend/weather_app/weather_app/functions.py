from .models import WeatherInfo



####################
### Guardar en la DB
####################

def guardar_datos_en_db(weather_info):
    # Crea una instancia del modelo WeatherInfo y guárdala en la base de datos
    weather_info_db = WeatherInfo(
        country = weather_info.get('location', {}).get('country'),
        city = weather_info.get('location', {}).get('city'),
        longitude = weather_info.get('longitude'),
        latitude = weather_info.get('latitude'),
        temperature = weather_info.get('temperature', {}).get('celsius'),
        feels_like = weather_info.get('temperature', {}).get('feels_like'),
        temp_min = weather_info.get('temperature', {}).get('temp_min'),
        temp_max = weather_info.get('temperature', {}).get('temp_max'),
        humidity = weather_info.get('humidity'),
        sunrise = weather_info.get('sun', {}).get('sunrise'),
        sunset = weather_info.get('sun', {}).get('sunset'),
        description = weather_info.get('description'),
        api_url = weather_info.get('api_url'),
    )

    # Guardar en la base de datos
    weather_info_db.save()

    # Devuelve una respuesta JSON con los datos guardados
    return 'True'