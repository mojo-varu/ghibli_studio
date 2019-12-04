from django.test import TestCase, Client
from django.urls import reverse, resolve
from movies.views import MoviesView, MoviesPeopleMapping


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
        self.client = Client()
        self.movies_view_url = reverse('movies-list')
        self.people_mapping_url = reverse('movies-people-mapping')

        self.movies_view_template = 'movies/movies-list.html'

    def test_movies_view_GET(self):
        response = self.client.get(self.movies_view_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.movies_view_template)
        self.assertTrue(isinstance(response.context['movies'], list))
        self.assertNotEqual(len(response.context['movies']), 0)

    def test_people_mapping_view_GET(self):
        response = self.client.get(self.people_mapping_url)
        self.assertEqual(response.status_code, 200)


