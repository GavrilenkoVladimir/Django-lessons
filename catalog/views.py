from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, Http404
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
    paginate_by = 2


class AuthorListView(generic.ListView):
    model = Author

class BookDetailView(generic.DetailView):
    model = Book

