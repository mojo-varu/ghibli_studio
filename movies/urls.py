from django.urls import path
from movies.views import FilmList, MovieList

urlpatterns = [
    path("films/", FilmList.as_view(), name="film_list"),
    path("movies/", MovieList.as_view(), name="movie_list"),
]