from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField('название', max_length=200)
    photo = models.ImageField(upload_to='pokemon', null=True)

    def __str__(self):
        return f'{self.title}'

class PokemonEntity(models.Model):
    lat = models.FloatField("lat", max_length=200)
    lon = models.FloatField("long", max_length=200)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    appeared_at = models.DateTimeField("appeared_at")
    disappeared_at = models.DateTimeField("disappeared_at")
# your models here
