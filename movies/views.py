from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from django.core.cache import cache
from movies.dataservice import get_people_per_movie, get_films_people_mapping


class MoviesPeopleMapping(APIView):
    def get(self, request, *args, **kwargs):
        films_people = get_films_people_mapping()
        return Response(films_people,
                        status=status.HTTP_200_OK)


class MoviesView(APIView):
    def get(self, request, ):

        cache_key = 'ghibli_studio_cache'
        cache_time = 60
        result = cache.get(cache_key)

        if not result:
            result = get_people_per_movie()
            cache.set(cache_key, result, cache_time)

        return Response(result,
                        status=status.HTTP_200_OK)
