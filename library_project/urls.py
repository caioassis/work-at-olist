from django.urls import path, include
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    path('', include('library.urls')),
    path('docs/', include_docs_urls(title='Library API Project'))
]
