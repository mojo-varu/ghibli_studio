from django.conf import settings
import json
import requests
from movies import constants


class GhibliStudio:
    """ To consume information from Studio Ghibli API endpoints

    This class contains methods to retrieve information from films/ and people/
    endpoints provided by Studio Ghibli. Also it contains methods to create
    mapping on retrieved data as per one to many relationship between people
    and films, provided by people/ endpoint.
    """

    def __init__(self):
        self._api_base_url = settings.STUDIO_GHIBLI_BASE_URL
        self._films_endpoint = settings.SG_FILMS_ENDPOINT
        self._people_endpoint = settings.SG_PEOPLE_ENDPOINT
        self._limit_params = {'limit': '250'}

    def _get_movies(self):
        """
        To retrieve information about all of the Studio Ghibli films.
        """
        response = requests.get(self._api_base_url + self._films_endpoint,
                                params=self._limit_params)
        if response.status_code != requests.codes.ok:
            return

        movies = json.loads(response.text)
        return movies

    def _get_people(self):
        """
        To retrieve information about all of the Studio Ghibli people.
        """
        response = requests.get(self._api_base_url + self._people_endpoint,
                                params=self._limit_params)
        if response.status_code != requests.codes.ok:
            return

        people = json.loads(response.text)
        return people

    def get_movies_people_mapping(self):
        """
        To create a mapping, based on one to many relationship between people
        and films as provided by the people/ endpoint of Studio Ghibli.
        """
        people = self._get_people()
        if not people:
            return

        movies_people_mapping = {}
        for person in people:
            person_name = person.get(constants.people_name)
            movies_performed = person.get(constants.people_films)

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
        """
        Returns a list containing  movies mapped to people performed in each
        movie.
        """
        movies = self._get_movies()
        if not movies:
            return

        movies_with_people = self.get_movies_people_mapping()
        if not movies_with_people:
            return

        people_per_movie = []
        for movie in movies:
            people_per_movie.append({constants.movie_name: movie.get(
                constants.film_title), constants.people_performed:
                movies_with_people.get(movie.get(constants.film_id))})

        return people_per_movie

