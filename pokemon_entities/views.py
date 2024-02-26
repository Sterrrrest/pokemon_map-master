import folium
import json
from django.utils.timezone import localtime
from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotFound
from django.shortcuts import render
from pokemon_entities.models import Pokemon, PokemonEntity
from django.http import HttpRequest, request

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon,image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    pokemons_entities = PokemonEntity.objects.all()
    visible_pokemons = pokemons_entities.filter(appeared_at__lt=localtime(), disappeared_at__gt=localtime())

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for visible_pokemon in visible_pokemons:
        add_pokemon(
            folium_map, visible_pokemon.lat,
            visible_pokemon.lon,
            visible_pokemon.pokemon.photo.path
        )

    pokemons_on_page = []
    for visible_pokemon in visible_pokemons:
        pokemons_on_page.append({
            'pokemon_id': visible_pokemon.pokemon.id,
            'img_url': visible_pokemon.pokemon.photo.path,
            'title_ru': visible_pokemon.pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    # with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    pokemons = Pokemon.objects.all()
    pokemons_entities = PokemonEntity.objects.all()
    pokemon_entity = pokemons_entities.get(pokemon=pokemon)


    # for pokemon in pokemons:
    #     if pokemon['pokemon_id'] == int(pokemon_id):
    #         requested_pokemon = pokemon
    #         break
    # else:
    #     return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    add_pokemon(
        folium_map, pokemon_entity.lat,
        pokemon_entity.lon,
        pokemon.photo.path,
    )

    # pokemons_on_page = []
    pokemons_on_page = ({
        'pokemon_id': pokemon.id,
        'img_url': pokemon.photo.path,
        'title_ru': pokemon.title,
        'description': pokemon.description,
    })

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemons_on_page
    })
