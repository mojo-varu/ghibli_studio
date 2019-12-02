from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
import requests
import json

from movies.models import Film, Person
from movies.serializers import FilmSerializer, PersonSerializer


class FilmList(APIView):
    serializer_class = FilmSerializer

    def get(self, request, ):
        response = requests.get('https://ghibliapi.herokuapp.com/films/',
                                params={'limit': '250'})
        print("Films Response Status : ", response.status_code)
        films = json.loads(response.text)
        for film in films:
            serializer = FilmSerializer(data=film)
            if serializer.is_valid():
                serializer.save()
            else:
                pass

        resp = requests.get('https://ghibliapi.herokuapp.com/people/',
                            params={'limit': '250'})

        people = json.loads(resp.text)
        print("People Response Status : ", resp.status_code)
        for person in people:
            film_urls = person['films']
            updated_films = []
            for film_url in film_urls:
                film_id = film_url.split('/')[-1]
                film_title = Film.objects.get(id=film_id)
                updated_films.append({'id': film_id,
                                      'title': film_title.get_title()})

            person['films'] = updated_films
            serializer = PersonSerializer(data=person)
            if serializer.is_valid():
                serializer.save()
            else:
                print(serializer.errors)

        return Response("God knows",
                        status=status.HTTP_200_OK)


class MovieList(APIView):

    @cache_page(60*2)
    def get(self, request, ):
        return Response("Coming soon", status=status.HTTP_200_OK)
