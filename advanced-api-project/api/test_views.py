from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from .models import Author, Book
from django.contrib.auth import get_user_model


class BookAPITests(APITestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="tester", email="tester@example.com", password="secret123"
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.author1 = Author.objects.create(name="Chinua Achebe")
        self.author2 = Author.objects.create(name="J. R. R. Tolkien")
        self.book1 = Book.objects.create(
            title="Things Fall Apart", publication_year=1958, author=self.author1
        )
        self.book2 = Book.objects.create(
            title="No Longer at Ease", publication_year=1960, author=self.author1
        )
        self.book3 = Book.objects.create(
            title="The Hobbit", publication_year=1937, author=self.author2
        )
        self.list_url = reverse("book-list")
        self.detail_url = lambda pk: reverse("book-detail", kwargs={"pk": pk})
        self.create_url = reverse("book-create")
        self.update_url = lambda pk: reverse("book-update", kwargs={"pk": pk})
        self.delete_url = lambda pk: reverse("book-delete", kwargs={"pk": pk})
        self.auth_header = {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}


    def test_list_books_public_access(self):
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)

    def test_retrieve_book_public_access(self):
        res = self.client.get(self.detail_url(self.book1.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["title"], "Things Fall Apart")

    def test_cannot_create_book_without_auth(self):
        payload = {
            "title": "Purple Hibiscus",
            "publication_year": 2003,
            "author": self.author1.id,
        }
        res = self.client.post(self.create_url, payload, format="json")
        self.assertIn(res.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_cannot_update_book_without_auth(self):
        payload = {"title": "Things Fall Apart (Edited)", "publication_year": 1958, "author": self.author1.id}
        res = self.client.put(self.update_url(self.book1.id), payload, format="json")
        self.assertIn(res.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_cannot_delete_book_without_auth(self):
        res = self.client.delete(self.delete_url(self.book1.id))
        self.assertIn(res.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))


    def test_create_book_with_auth(self):
        payload = {
            "title": "Half of a Yellow Sun",
            "publication_year": 2006,
            "author": self.author1.id,
        }
        res = self.client.post(self.create_url, payload, format="json", **self.auth_header)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["title"], payload["title"])
        self.assertEqual(res.data["publication_year"], payload["publication_year"])
        self.assertEqual(res.data["author"], payload["author"])

    def test_update_book_with_auth(self):
        payload = {
            "title": "Things Fall Apart (Updated)",
            "publication_year": 1958,
            "author": self.author1.id,
        }
        res = self.client.put(self.update_url(self.book1.id), payload, format="json", **self.auth_header)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, payload["title"])

    def test_delete_book_with_auth(self):
        res = self.client.delete(self.delete_url(self.book2.id), **self.auth_header)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book2.id).exists())


    def test_reject_future_publication_year(self):
        future_year = timezone.now().year + 5
        payload = {
            "title": "From The Future",
            "publication_year": future_year,
            "author": self.author1.id,
        }
        res = self.client.post(self.create_url, payload, format="json", **self.auth_header)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("publication_year", res.data)



    def test_filter_by_author_name(self):
        res = self.client.get(self.list_url, {"author__name": "Chinua Achebe"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in res.data]
        self.assertCountEqual(titles, ["Things Fall Apart", "No Longer at Ease"])

    def test_search_by_title(self):
        res = self.client.get(self.list_url, {"search": "hobbit"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["title"], "The Hobbit")

    def test_order_by_publication_year_desc(self):
        res = self.client.get(self.list_url, {"ordering": "-publication_year"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in res.data]
        self.assertEqual(years, sorted(years, reverse=True))
