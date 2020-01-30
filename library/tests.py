import os
from django.core.management import call_command
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from .models import Author


class AuthorTestCase(TestCase):

    def test_create_new_author(self):
        author = Author.objects.create(name='Dan Brown')
        self.assertEqual(author.name, 'Dan Brown')
        authors = Author.objects.all()
        self.assertEqual(authors.count(), 1)  # Only 1 author is expected to be in database

    def test_import_authors_command(self):
        """
        Creates an .csv file, tests if import works successfully and removes the file.
        :return:
        """
        content = 'name\n'
        authors = ['J. K. Rowling', 'Dan Brown', 'George R. R. Martin']
        content += '\n'.join(iter(authors))
        filename = 'authors.csv'
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        call_command('import_authors', filename)
        os.remove(filename)
        authors = Author.objects.all()
        self.assertEqual(authors.count(), len(authors))


class AuthorAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        Author.objects.bulk_create(
            [
                Author(name='J. K. Rowling'),
                Author(name='Dan Brown')
            ]
        )

    def test_author_list_view(self):
        response = self.client.get('/authors/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        expected_author_id_list = [1, 2]
        author_id_list = list(map(lambda author: author['id'], response.data))
        self.assertEqual(expected_author_id_list, author_id_list)

    def test_retrieve_author_view(self):
        author_id = 1
        response = self.client.get(f'/authors/{author_id}/')
        self.assertEqual(response.status_code, 200)
        author = Author.objects.get(pk=author_id)
        self.assertEqual(response.data['id'], author.pk)
        self.assertEqual(response.data['name'], author.name)

    def test_author_does_not_exist_returns_404(self):
        response = self.client.get('/authors/50/')
        self.assertEqual(response.status_code, 404)
