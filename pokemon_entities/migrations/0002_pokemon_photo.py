# Generated by Django 3.1.14 on 2024-02-24 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='photo',
            field=models.ImageField(null=True, upload_to='pokemon'),
        ),
    ]