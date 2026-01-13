from django.urls import path
from django.utils.http import parse_http_date

from catalog.views import (
    index,
    LiteraryFormatView,
    BookListView,
    AuthorListView,
    BookDetailView,
    test_session_view,
    AuthorDetailView,
    LiteraryFormatCreateView,
    LiteraryFormatUpdateView,
    LiteraryFormatDeleteView,
)

urlpatterns = [
    path("", index, name="index"),
    path("literary-formats/", LiteraryFormatView.as_view(), name="literary-format-list"),
    path("literary-formats/create/", LiteraryFormatCreateView.as_view(), name="literary-format-create"),
    path("literary-formats/<int:pk>/update/", LiteraryFormatUpdateView.as_view(), name="literary-format-update"),
    path("literary-formats/<int:pk>/delete/", LiteraryFormatDeleteView.as_view(), name="literary-format-delete"),
    path("books/", BookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("authors/", AuthorListView.as_view(), name="author-list"),
    path("authtors/<int:pk>/", AuthorDetailView.as_view(), name="author-detail"),
    path("test-session/", test_session_view, name="test-session"),

]

app_name = "catalog"
