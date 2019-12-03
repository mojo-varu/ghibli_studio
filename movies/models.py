from django.db import models


class Film(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_film_title(self):
        return self.title


class Person(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_person_name(self):
        return self.name
