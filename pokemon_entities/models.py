from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField('название', max_length=200)
    photo = models.ImageField(upload_to='pokemon', null=True)

    def __str__(self):
        return f'{self.title}'

class PokemonEntity(models.Model):
    lat = models.FloatField("lat", max_length=200)
    lon = models.FloatField("lon", max_length=200)
# your models here
