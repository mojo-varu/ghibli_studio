from django.conf import settings
import json
import requests


class GhibliStudio:

    def __init__(self):
        self._api_base_url = settings.STUDIO_GHIBLI_BASE_URL
        self._limit_params = {'limit': '250'}

    def _get_movies(self):
        response = requests.get(self._api_base_url+'/films/',
                                params=self._limit_params)
        if response.status_code != requests.codes.ok:
            return

        movies = json.loads(response.text)
        return movies

    def _get_people(self):
        response = requests.get(self._api_base_url + '/people/',
                                params=self._limit_params)
        if response.status_code != requests.codes.ok:
            return

        people = json.loads(response.text)
        return people

    def get_movies_people_mapping(self):
        people = self._get_people()
        if not people:
            return

        movies_people_mapping = {}
        for person in people:
            person_name = person.get('name')
            movies_performed = person.get('films')

            if not movies_performed:
                continue

            for movie_url in movies_performed:
                movie_id = movie_url.split('/')[-1]
                if movie_id not in movies_people_mapping:
                    movies_people_mapping[movie_id] = [person_name]
                else:
                    movies_people_mapping.get(movie_id).append(person_name)

        return movies_people_mapping

    def get_people_per_movie(self):
        movies = self._get_movies()
        if not movies:
            return

        movies_with_people = self.get_movies_people_mapping()
        if not movies_with_people:
            return

        people_per_movie = []
        for movie in movies:
            people_per_movie.append({'movie_name': movie.get('title'),
                                     'people_performed':
                                         movies_with_people.get(
                                             movie.get('id'))})

        return people_per_movie

