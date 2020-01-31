import os
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from .models import Author, Book


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


class BookTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author1 = Author.objects.create(name='Dan Brown')
        cls.author2 = Author.objects.create(name='J. K. Rowling')
        cls.author3 = Author.objects.create(name='George R. R. Martin')

    def test_create_new_book(self):
        book = Book.objects.create(name='Book 1', publication_year=timezone.now().year)
        book.authors.set([self.author1, self.author2])
        self.assertEqual(book.name, 'Book 1')
        self.assertEqual(book.edition, 1)
        self.assertIn(self.author1, book.authors.all())
        self.assertNotIn(self.author3, book.authors.all())
        self.assertEqual(book.authors.count(), 2)

    def test_delete_book(self):
        Book.objects.bulk_create(
            [
                Book(name='Book 1', publication_year=timezone.now().year),
                Book(name='Book 2', publication_year=timezone.now().year-1),
                Book(name='Book 3', publication_year=timezone.now().year-2),
                Book(name='Book 4', publication_year=timezone.now().year-3)
            ]
        )
        books = Book.objects.all()
        books.first().delete()
        self.assertEqual(books.count(), 3)
        books.delete()
        self.assertEqual(books.count(), 0)


class BookAPITestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.author1 = Author.objects.create(name='Dan Brown')
        cls.author2 = Author.objects.create(name='J. K. Rowling')
        cls.author3 = Author.objects.create(name='George R. R. Martin')
        cls.book = Book.objects.create(name='Book 1', edition=1, publication_year=timezone.now().year)
        cls.book.authors.set([cls.author1, cls.author2])

    def test_book_list_view(self):
        response = self.client.get('/books/')
        self.assertEqual(len(response.data), 1)
        Book.objects.create(name='Book 2', edition=1, publication_year=timezone.now().year)
        response = self.client.get('/books/')
        self.assertEqual(len(response.data), 2)

    def test_create_new_book(self):
        book = {'name': 'Book 2', 'edition': 2, 'publication_year': 1920, 'authors': [self.author3.pk]}
        response = self.client.post('/books/', book, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['id'], 2)
        self.assertEqual(Book.objects.all().count(), 2)
        self.assertNotIn([self.author1.pk, self.author2.pk], response.data['authors'])
        self.assertIn(self.author3.pk, response.data['authors'])

    def test_update_book(self):
        book_id = self.book.pk
        response = self.client.patch(f'/books/{book_id}/', {'name': 'New Book'}, content_type='application/json')
        updated_book = Book.objects.get(pk=book_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_book.name, 'New Book')

    def test_delete_book(self):
        book_id = self.book.pk
        response = self.client.delete(f'/books/{book_id}/')
        self.assertEqual(response.status_code, 204)  # Returns no content
        book_count = Book.objects.all().count()
        self.assertEqual(book_count, 0)
