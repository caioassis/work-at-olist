from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from .models import Author
from .serializers import AuthorSerializer


class AuthorViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
