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
    pokemons_entities = PokemonEntity.objects.all()
    current_time = localtime()
    visible_pokemons = pokemons_entities.filter(appeared_at__lt=current_time, disappeared_at__gt=current_time)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for visible_pokemon in visible_pokemons:
        add_pokemon(
            folium_map, visible_pokemon.lat,
            visible_pokemon.lon,
            request.build_absolute_uri(visible_pokemon.pokemon.photo.url)
        )

    pokemons_on_page = []
    for visible_pokemon in visible_pokemons:
        pokemons_on_page.append({
            'pokemon_id': visible_pokemon.pokemon.id,
            'img_url': request.build_absolute_uri(visible_pokemon.pokemon.photo.url),
            'title_ru': visible_pokemon.pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    pokemons_entities = PokemonEntity.objects.all()
    pokemon_entity = pokemons_entities.get(pokemon=pokemon)


    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    add_pokemon(
        folium_map, pokemon_entity.lat,
        pokemon_entity.lon,
        pokemon.photo.path,
    )

    if pokemon.previous_evolution is None:
        pokemons_on_page = ({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.photo.url),
            'title_ru': pokemon.title_ru,
            'title_en': pokemon.title_en,
            'title_jp': pokemon.title_jp,
            'description': pokemon.description,
            'next_evolution':
                {
                    "title_ru": pokemon.Pokemon.all()[0].title_ru,
                    "pokemon_id": pokemon.Pokemon.all()[0].id,
                    "img_url": request.build_absolute_uri(pokemon.Pokemon.all()[0].photo.url)
                },
        })
    elif not pokemon.Pokemon.all():
        pokemons_on_page = ({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.photo.url),
            'title_ru': pokemon.title_ru,
            'title_en': pokemon.title_en,
            'title_jp': pokemon.title_jp,
            'description': pokemon.description,
            'previous_evolution': {
                "title_ru": pokemon.previous_evolution.title_ru,
                "pokemon_id": pokemon.previous_evolution.id,
                "img_url": request.build_absolute_uri(pokemon.previous_evolution.photo.url)
            },
    })
    else:
        pokemons_on_page = ({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.photo.url),
            'title_ru': pokemon.title_ru,
            'title_en': pokemon.title_en,
            'title_jp': pokemon.title_jp,
            'description': pokemon.description,
            'previous_evolution':
                {
                    "title_ru": pokemon.previous_evolution.title_ru,
                    "pokemon_id": pokemon.previous_evolution.id,
                    "img_url": request.build_absolute_uri(pokemon.previous_evolution.photo.url)
                },
            'next_evolution':
                {
                    "title_ru": pokemon.Pokemon.all()[0].title_ru,
                    "pokemon_id": pokemon.Pokemon.all()[0].id,
                    "img_url": request.build_absolute_uri(pokemon.Pokemon.all()[0].photo.url)
                },
        })



    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemons_on_page
    })
