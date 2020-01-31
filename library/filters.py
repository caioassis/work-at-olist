from django_filters.filterset import FilterSet
from .models import Author, Book


class AuthorFilterSet(FilterSet):

    class Meta:
        model = Author
        fields = {
            'name': ['exact', 'icontains']
        }


class BookFilterSet(FilterSet):

    class Meta:
        model = Book
        fields = {
            'name': ['exact', 'icontains'],
            'edition': ['exact'],
            'publication_year': ['exact'],
            'authors': ['exact']
        }
