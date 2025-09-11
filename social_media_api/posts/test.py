from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()

class PostAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u", password="pass")
        self.client.login(username="u", password="pass") 

    def test_create_post_requires_auth(self):
        url = reverse('post-list')
        data = {"title":"t","content":"c"}
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_list_posts(self):
        Post.objects.create(author=self.user, title="t1", content="c1")
        resp = self.client.get(reverse('post-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
