from django.test import TestCase
from .models import Author


class AuthorTestCase(TestCase):

    def test_create_new_author(self):
        author = Author.objects.create(name='Dan Brown')
        self.assertEqual(author.name, 'Dan Brown')
        authors = Author.objects.all()
        self.assertEqual(authors.count(), 1)  # Only 1 author is expected to be in database
