from django.conf import settings

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.core.cache import cache

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from movies.dataservice import GhibliStudio


class MoviesPeopleMapping(APIView):
    def get(self, request, *args, **kwargs):
        ghibli_studio = GhibliStudio()
        movies_people = ghibli_studio.get_movies_people_mapping()
        if not movies_people:
            return Response('People are unpredictable, they go missing !',
                            status=status.HTTP_404_NOT_FOUND)

        return Response(movies_people, status=status.HTTP_200_OK)


class MoviesView(APIView):
    def get(self, request, *args, **kwargs):
        result = cache.get(settings.CACHE_KEY)
        if not result:
            ghibli_studio = GhibliStudio()
            result = ghibli_studio.get_people_per_movie()
            cache.set(settings.CACHE_KEY, result,
                      settings.CACHE_TIMEOUT_IN_SECS)
        if not result:
            return HttpResponseNotFound('<h2>Something wrong with movies !<br>'
                                        'Meanwhile read books until '
                                        'we fix this.</h2>')

        return render(request, 'movies/movies-list.html',
                      {'movies': result})
