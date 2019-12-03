from django.conf import settings
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

        result = cache.get(settings.CACHE_KEY)
        if not result:
            result = get_people_per_movie()
            cache.set(settings.CACHE_KEY, result,
                      settings.CACHE_TIMEOUT_IN_SECS)

        return Response(result,
                        status=status.HTTP_200_OK)
