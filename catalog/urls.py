from django.urls import path
from django.utils.http import parse_http_date

from catalog.views import index, LiteraryFormatView, BookListView, AuthorListView

urlpatterns = [
    path("", index, name="index"),
    path("literaty-formats/", LiteraryFormatView.as_view(), name="library-formats-list"),
    path("books/", BookListView.as_view(), name="book-list"),
    path("authors/", AuthorListView.as_view(), name="author-list"),

]

app_name = "catalog"
