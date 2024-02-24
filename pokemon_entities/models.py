from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField('название', max_length=200)
    photo = models.ImageField(upload_to='pokemon', null=True)

    def __str__(self):
        return f'{self.title}'


# your models here
