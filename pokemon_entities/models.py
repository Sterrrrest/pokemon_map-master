from django.db import models  # noqa F401


class Pokemon(models.Model):
    title_ru = models.CharField('название', max_length=200)
    title_jp = models.CharField('японское название', max_length=200, blank=True)
    title_en = models.CharField('английское название', max_length=200, blank=True)
    photo = models.ImageField(verbose_name='Фото', upload_to='Downloads', null=True)
    description = models.TextField("описание")
    previous_evolution = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Предыдущая эволюция', blank=True,
                                           null=True, related_name='Pokemon')


    def __str__(self):
        return self.title_ru

class PokemonEntity(models.Model):
    lat = models.FloatField("lat")
    lon = models.FloatField("lon")
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='PokemonEntity')
    appeared_at = models.DateTimeField("appeared_at")
    disappeared_at = models.DateTimeField("disappeared_at")
    level = models.IntegerField("уровень", null=True, blank=True)
    health = models.IntegerField("здоровье", null=True, blank=True)
    attack = models.IntegerField("атака", null=True, blank=True)
    defense = models.IntegerField("защита", null=True, blank=True)
    stamina = models.IntegerField("выносливость", null=True, blank=True)


    def __str__(self):
        return self.pokemon.title_ru
