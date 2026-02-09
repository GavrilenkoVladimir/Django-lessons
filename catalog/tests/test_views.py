from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import  TestCase

from catalog.models import LiteraryFormat, Book

LITERARY_FORMAT_URL = reverse("catalog:literary-format-list")
BOOK_LIST_URL = reverse("catalog:book-list")
AUTHOR_CREATE_FORM_URL = reverse("catalog:author-create")


class PublicLiteraryFormatTest(TestCase):
    def test_login_required(self):
        response = self.client.get(LITERARY_FORMAT_URL)
        self.assertNotEqual(response.status_code, 200)


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


class PrivateAuthorTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123",
        )
        self.client.force_login(self.user)

    def test_create_author(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "pseudonym": "Test pseudonym",
        }
        self.client.post(AUTHOR_CREATE_FORM_URL, data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.username, "new_user")

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.pseudonym, form_data["pseudonym"])
