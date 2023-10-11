from .models import WeatherInfo

import sqlite3

####################
### Guardar en la DB
####################

def guardar_datos_en_db2(weather_info):
    import sqlite3

    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()

    country = weather_info.get('location', {}).get('country')
    city = weather_info.get('location', {}).get('city')
    longitude = weather_info.get('longitude')
    latitude = weather_info.get('latitude')
    temperature = weather_info.get('temperature', {}).get('celsius')
    feels_like = weather_info.get('temperature', {}).get('feels_like')
    temp_min = weather_info.get('temperature', {}).get('temp_min')
    temp_max = weather_info.get('temperature', {}).get('temp_max')
    humidity = weather_info.get('humidity')
    sunrise = weather_info.get('sun', {}).get('sunrise')
    sunset = weather_info.get('sun', {}).get('sunset')
    description = weather_info.get('description')
    api_url = weather_info.get('api_url')

    # Crear una tupla de datos con los valores
    data = (country, city, longitude, latitude, temperature, feels_like, temp_min, temp_max, humidity, sunrise, sunset, description, api_url)

    cursor.execute("INSERT INTO weather_app_weatherinfo (country, city, longitude, latitude, temperature, feels_like, temp_min, temp_max, humidity, sunrise, sunset, description, api_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)

    conn.commit()
    conn.close()
    return 'true'


# por alguna razon misteriosa que desconozco, dejo de funcionar: guardar_datos_en_db(weather_info)
def guardar_datos_en_db(weather_info):
    try:
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

        print(weather_info_db)

        # Guardar en la base de datos
        weather_info_db.save()

        # Devuelve una respuesta JSON con los datos guardados
        return 'true'

    except Exception as e:
        # En caso de error, por ejemplo, si ya existe un registro con la misma clave primaria
        # Devuelve un mensaje de error o lanza una excepción personalizada si es necesario
        return 'Error al guardar datos en la base de datos: ' + str(e)