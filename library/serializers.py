from rest_framework.serializers import ModelSerializer
from .models import Author, Book


class AuthorSerializer(ModelSerializer):

    class Meta:
        model = Author
        fields = ['id', 'name']
        read_only_fields = ['id', 'name']


class BookListSerializer(ModelSerializer):
    authors = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'edition', 'publication_year', 'authors']
        read_only_fields = ['id', 'name', 'edition', 'publication_year', 'authors']


class BookSerializer(ModelSerializer):

    class Meta:
        model = Book
        fields = ['id', 'name', 'edition', 'publication_year', 'authors']
