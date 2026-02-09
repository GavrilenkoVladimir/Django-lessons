from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client, TestCase

from catalog.models import LiteraryFormat, Book

LITERARY_FORMAT_URL = reverse("catalog:literary-format-list")
BOOK_LIST_URL = reverse("catalog:book-list")


class PublicLiteraryFormatTest(TestCase):
    def test_login_required(self):
        response = self.client.get(LITERARY_FORMAT_URL)
        self.assertEqual(response.status_code, 200)


class PrivateLiteraryFormatTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_literary_formats(self):
        LiteraryFormat.objects.create(name="drama")
        LiteraryFormat.objects.create(name="poetry")
        response = self.client.get(LITERARY_FORMAT_URL)
        self.assertEqual(response.status_code, 200)
        literary_format = LiteraryFormat.objects.all()
        self.assertEqual(
            list(response.context["literary_format_list"]),
            list(literary_format),
        )
        self.assertTemplateUsed(response, "catalog/literary_format_list.html")


class BookListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

        self.literary_format = LiteraryFormat.objects.create(name="drama")

        self.book_1 = Book.objects.create(
            title="test1",
            price=100,
            format=self.literary_format,
        )
        self.book_1.authors.add(self.user)

        self.book_2 = Book.objects.create(
            title="test2",
            price=100,
            format=self.literary_format,
        )
        self.book_2.authors.add(self.user)

    def test_book_list_login_required(self):
        response = self.client.get(BOOK_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_book_list_search(self):
        response = self.client.get(
            BOOK_LIST_URL,
            {"title": "test1"}
        )

        self.assertEqual(response.status_code, 200)

        book_list = response.context["book_list"]

        self.assertEqual(list(book_list), [self.book_1])
