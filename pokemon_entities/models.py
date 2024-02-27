from django.db import models  # noqa F401


class Pokemon(models.Model):
    title_ru = models.CharField('название', max_length=200)
    title_jp = models.CharField('японское название', max_length=200, blank=True)
    title_en = models.CharField('английское название', max_length=200, blank=True)
    photo = models.ImageField(upload_to='Downloads', null=True, default=None)
    description = models.TextField("описание", max_length=1000, blank=True)
    # next_evolution = models.ForeignKey(blank=True, null=True, related_name='previous_evolution')
    previous_evolution = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True,
                                           null=True, related_name='Pokemon')
    level = models.IntegerField("уровень", blank=True)
    health = models.IntegerField("здоровье", blank=True)
    attack = models.IntegerField("атака", blank=True)
    defense = models.IntegerField("защита", blank=True)
    stamina = models.IntegerField("выносливость", blank=True)


    def __str__(self):
        return f'{self.title_ru}'

class PokemonEntity(models.Model):
    lat = models.FloatField("lat", max_length=200)
    lon = models.FloatField("lon", max_length=200)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    appeared_at = models.DateTimeField("appeared_at")
    disappeared_at = models.DateTimeField("disappeared_at")
# your models here
