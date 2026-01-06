from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from .models import Book, Author, LiteraryFormat


def index(request: HttpRequest) -> HttpResponse:
    num_books = Book.objects.count()
    num_authors = Author.objects.count()
    num_literary_formats = LiteraryFormat.objects.count()
    context = {
        "num_books": num_books,
        "num_authors": num_authors,
        "num_literary_formats": num_literary_formats,
    }
    return render(request, "catalog/index.html", context=context)

class LiteraryFormatView(generic.ListView):
    model = LiteraryFormat
    template_name = "catalog/literary_format_list.html"
    context_object_name = "literary_format_list"
    queryset = LiteraryFormat.objects.all()


class BookListView(generic.ListView):
    model = Book
    queryset = Book.objects.select_related("format")


class AuthorListView(generic.ListView):
    model = Author


def book_detail_view(request: HttpRequest, pk: int):
    book = Book.objects.get(pk=pk)
    context = {
        "book": book,
    }
    return render(request, "catalog/book_detail.html/", context=context)
