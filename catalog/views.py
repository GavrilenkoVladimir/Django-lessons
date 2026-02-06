from django.contrib.auth import user_login_failed
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import AuthorCreationForm, BookForm, BookSearchForm
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


class LiteraryFormatCreateView(LoginRequiredMixin, generic.CreateView):
    model = LiteraryFormat
    fields = "__all__"
    success_url = reverse_lazy("catalog:literary-format-list")
    template_name = "catalog/literary_format_form.html"


class LiteraryFormatUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = LiteraryFormat
    fields = "__all__"
    success_url = reverse_lazy("catalog:literary-format-list")
    template_name = "catalog/literary_format_form.html"


class LiteraryFormatDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = LiteraryFormat
    template_name = "catalog/literary_format_confirm_delete.html"
    success_url = reverse_lazy("catalog:literary-format-list")


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["title"] = title
        context["search_form"] = BookSearchForm(
            initial={"title": title}
        )
        return context

    def get_queryset(self):
        queryset = Book.objects.select_related("format")
        # title = self.request.GET.get("title")
        # if title:
        #     return self.queryset.filter(title__icontains=title)
        # return self.queryset
        form = BookSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                title__icontains=form.cleaned_data["title"]
            )
        return queryset


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book


class BookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Book
    form_class = BookForm

class BookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Book
    form_class = BookForm


class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    paginate_by = 2


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author
    queryset = Author.objects.prefetch_related("books")


class AuthorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Author
    form_class = AuthorCreationForm

    def get_success_url(self):
        return reverse_lazy("catalog:author-detail", kwargs={"pk": self.object.pk})