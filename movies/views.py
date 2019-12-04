from django.conf import settings

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.core.cache import cache

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from movies.dataservice import GhibliStudio
from movies import constants


class MoviesView(APIView):
    """ Gives a list of, names of movies mapped to names people performed in
    each movie.

    This class contains only a GET method. The implementation of this GET
    method has a caching mechanism, implemented using memcached.
    There are 2 major purpose of using memcached here -
        1. Its an in-memory cache, so retrieval is very fast compared to
        other alternatives for cache like database or file system.
        2. Cache can be set to automatic expiry timeout, which suits well for
        use cases where fresh data needs to cached after certain time interval

    Redis is another good alternative for in-memory cache.

    Explanation for this approach -
    In order to provide updated information in every 60 secs to our movie
    buffs, we need to periodically check for new information at ghibli studio,
    Given the only source of truth here is Ghibli's API and there is a short
    refresh window, writing data into database will cost performance and might
    require changes in schema as per changes API. Plus with current use case
    there is no use of storing all the information about movies and people.
    Also running a periodic task is not a viable option here.

    With our current implementation we need to hit Ghibli's API only once on
    each cache miss.
    """

    def get(self, request, *args, **kwargs):
        """ Returns result from cache, in case of cache-miss, which happens on
            cache expiry, it fetches fresh data from Ghibli studio, sets that
            into cache with new TIMEOUT and returns the results. Consecutive
            requests are served from cache til the expires again.
        """
        result = cache.get(settings.CACHE_KEY)
        if not result:
            ghibli_studio = GhibliStudio()
            result = ghibli_studio.get_people_per_movie()
            cache.set(settings.CACHE_KEY, result,
                      settings.CACHE_TIMEOUT_IN_SECS)
        if not result:
            return HttpResponseNotFound(constants.movies_missing)

        return render(request, constants.movies_template,
                      {constants.movies: result})


class MoviesPeopleMapping(APIView):
    """
    This class contains a GET method that provides mapping between movies and
    people, based on movie ID. The purpose of this endpoint is to determine
    relationship between movies and people.
    """

    def get(self, request, *args, **kwargs):
        """ Returns a dictionary of movies, with movie id as key and
            list of people name as value
        """
        ghibli_studio = GhibliStudio()
        movies_people = ghibli_studio.get_movies_people_mapping()
        if not movies_people:
            return Response(constants.people_missing,
                            status=status.HTTP_404_NOT_FOUND)

        return Response(movies_people, status=status.HTTP_200_OK)