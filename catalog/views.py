from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render
from django.views import generic

from .models import Book, Author, LiteraryFormat

@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_books = Book.objects.count()
    num_authors = Author.objects.count()
    num_literary_formats = LiteraryFormat.objects.count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    context = {
        "num_books": num_books,
        "num_authors": num_authors,
        "num_literary_formats": num_literary_formats,
        "num_visits": request.session["num_visits"],
    }
    return render(request, "catalog/index.html", context=context)

class LiteraryFormatView(LoginRequiredMixin, generic.ListView):
    model = LiteraryFormat
    template_name = "catalog/literary_format_list.html"
    context_object_name = "literary_format_list"
    queryset = LiteraryFormat.objects.all()
    paginate_by = 2


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    queryset = Book.objects.select_related("format")
    paginate_by = 2


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book


class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    paginate_by = 2


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author
    queryset = Author.objects.prefetch_related("books")


def test_session_view(request):
    return HttpResponse(
        "<h1>Test Session</h1>"
        f"<h4>Session data: {request.session['book']}</h4>"
    )



