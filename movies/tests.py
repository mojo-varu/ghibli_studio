from django.test import TestCase, Client as DjangoClient
from django.urls import reverse, resolve
from movies.views import MoviesView, MoviesPeopleMapping

from memcache import Client as MemClient

""" 
Suggestion - 
Right now the unit tests are hitting Ghibili API.
This can be mocking request/response of Ghibili API
"""


class TestUrls(TestCase):
    """ Tests that URLs in movies app resolves to correct views """

    def test_movies_list_url(self):
        url = reverse('movies-list')
        self.assertEqual(resolve(url).func.view_class, MoviesView)

    def test_movies_people_mapping_url(self):
        url = reverse('movies-people-mapping')
        self.assertEqual(resolve(url).func.view_class, MoviesPeopleMapping)


class TestViews(TestCase):
    """ Tests that the response of the views are valid  """

    def setUp(self):
        self.client = DjangoClient()
        self.movies_view_url = reverse('movies-list')
        self.people_mapping_url = reverse('movies-people-mapping')
        self.movies_view_template = 'movies/movies-list.html'

    def test_movies_view_GET(self):
        response = self.client.get(self.movies_view_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.movies_view_template)
        self.assertTrue(isinstance(response.context['movies'], list))

    def test_people_mapping_view_GET(self):
        response = self.client.get(self.people_mapping_url)
        self.assertEqual(response.status_code, 200)


class TestMemcached(TestCase):
    """ Tests interaction with memcached server """

    def setUp(self):
        servers = ["memcached:11211"]
        self.mc = MemClient(servers, debug=1)

    def tearDown(self):
        self.mc.flush_all()
        self.mc.disconnect_all()

    def test_setget(self):
        key = "ghibli"
        val_gave = "studio"
        self.mc.set(key, val_gave, noreply=True)
        val_got = self.mc.get(key)
        self.assertEqual(val_got, val_got)
