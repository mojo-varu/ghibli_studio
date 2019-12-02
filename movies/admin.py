from django.contrib import admin
from movies.models import Film, Person


class FilmAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at')


class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')


admin.site.register(Film, FilmAdmin)
admin.site.register(Person, PersonAdmin)
