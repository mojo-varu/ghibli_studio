from django.conf import settings
import json
import requests
import datetime


def get_all_films():
    response = requests.get(settings.STUDIO_GHIBLI_BASE_URL+'/films/',
                            params={'limit': '250'})
    print("Films Response Status : ", response.status_code)
    films = json.loads(response.text)
    return films


def get_films_people_mapping():
    response = requests.get(settings.STUDIO_GHIBLI_BASE_URL+'/people/',
                            params={'limit': '250'})
    people = json.loads(response.text)
    movie_people_mapping = {}
    for person in people:
        for film_url in person['films']:
            film_id = film_url.split('/')[-1]
            if film_id not in movie_people_mapping.keys():
                movie_people_mapping[film_id] = [person['name']]
            else:
                movie_people_mapping.get(film_id).append(person['name'])

    return movie_people_mapping


def get_people_per_movie():
    films = get_all_films()
    movie_people_mapping = get_films_people_mapping()
    people_per_movie = []
    for film in films:
        people_per_movie.append({'movie_name': film['title'],
                                 'movie_id': film['id'],
                                 'people_in_movie':
                                     movie_people_mapping.get(film['id']),
                                 'updated_at':
                                     datetime.datetime.now().strftime(
                                         "%m/%d/%Y, %H:%M:%S")})
    return people_per_movie
