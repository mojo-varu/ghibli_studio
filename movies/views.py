from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from movies.dataservice import get_people_per_movie, get_films_people_mapping


class MoviesPeopleMapping(APIView):
    def get(self, request, *args, **kwargs):
        films_people = get_films_people_mapping()
        return Response(films_people,
                        status=status.HTTP_200_OK)


class MoviesView(APIView):
    def get(self, request, ):
        people_in_movie = get_people_per_movie()
        return Response(people_in_movie,
                        status=status.HTTP_200_OK)

