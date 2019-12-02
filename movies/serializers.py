from rest_framework import serializers
from movies.models import Film, Person


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
    films = FilmSerializer(many=True, required=False)

    class Meta:
        model = Person
        fields = '__all__'
