from django.urls import path
from movies.views import MoviesView, MoviesPeopleMapping

urlpatterns = [
    path("movies/", MoviesView.as_view(), name="movies-list"),
    path('people/', MoviesPeopleMapping.as_view(),
         name='movies-people-mapping'),
]