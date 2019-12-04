""" ghibli_studio URL Configuration """

from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    re_path(r'^', include('movies.urls')),
    path('admin/', admin.site.urls),
]
