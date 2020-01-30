from rest_framework.serializers import ModelSerializer
from .models import Author


class AuthorSerializer(ModelSerializer):

    class Meta:
        model = Author
        fields = ['id', 'name']
        read_only_fields = ['id', 'name']
