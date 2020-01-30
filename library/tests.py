from django.core.management import call_command
from django.test import TestCase
from .models import Author
import os
from io import StringIO


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
