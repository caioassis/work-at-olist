from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .filters import AuthorFilterSet, BookFilterSet
from .models import Author, Book
from .serializers import AuthorSerializer, BookListSerializer, BookSerializer


class AuthorViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    # pagination_class = PageNumberPagination
    filterset_class = AuthorFilterSet


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    filterset_class = BookFilterSet
    # pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return BookListSerializer
        return BookSerializer
