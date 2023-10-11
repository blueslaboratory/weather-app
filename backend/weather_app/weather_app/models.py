from django.db import models

class WeatherInfo(models.Model):
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    longitude = models.FloatField()
    latitude = models.FloatField()
    temperature = models.FloatField()
    feels_like = models.FloatField()
    temp_min = models.FloatField()
    temp_max = models.FloatField()
    humidity = models.IntegerField()
    sunrise = models.TimeField()
    sunset = models.TimeField()
    description = models.CharField(max_length=255)
    api_url = models.URLField()


    def __str__(self):
        return self.city
