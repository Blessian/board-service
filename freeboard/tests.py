from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from argon2 import PasswordHasher, exceptions

from freeboard.models import Article

success_data = {
    'title': '적당한 길이의 제목',
    'content': '적당한 길이의 내용',
    'password': 'pass11'
}

fail_data1 = {
    'title': '너무 긴 제목 너무 긴 제목 너무 긴 제목 너무 긴 제목 너무 긴 제목 너무 긴 제목 너무 긴 제목 너무 긴 제목 너무 긴 제목 '
             '너무 긴 제목 너무 긴 제목 너무 긴 제목 너무 긴 제목 너무 긴 제목 너무 긴 제목 너무 긴 제목 너무 긴 제목 너무 긴 제목 '
             '너무 긴 제목 너무 긴 제목 너무 긴 제목 너무 긴 제목 너무 긴 제목 너무 긴 제목 너무 긴 제목 너무 긴 제목 너무 긴 제목 ',
    'content': '적당한 길이의 내용',
    'password': 'pass11'
}

fail_data2 = {
    'title': '적당한 길이의 제목',
    'content': '너무 긴 내용 너무 긴 내용 너무 긴 내용 너무 긴 내용 너무 긴 내용 너무 긴 내용 너무 긴 내용 너무 긴 내용 너무 긴 내용 '
               '너무 긴 내용 너무 긴 내용 너무 긴 내용 너무 긴 내용 너무 긴 내용 너무 긴 내용 너무 긴 내용 너무 긴 내용 너무 긴 내용 '
               '너무 긴 내용 너무 긴 내용 너무 긴 내용 너무 긴 내용 너무 긴 내용 너무 긴 내용 너무 긴 내용 너무 긴 내용 너무 긴 내용 ',
    'password': 'pass11'
}

fail_data3 = {
    'title': '적당한 길이의 제목',
    'content': '적당한 길이의 내용',
    'password': '형식에 맞지 않는 비밀번호'
}


class SuccessTestCase(APITestCase):
    def setUp(self):
        hash_pass = PasswordHasher().hash('pass11')

        self.article = Article.objects.create(
            title='test',
            content='test',
            password=hash_pass
        )

    def test_list(self):
        responce = self.client.get(reverse('articles-list'))
        self.assertEqual(responce.status_code, status.HTTP_200_OK)

    def test_create(self):
        responce = self.client.post(reverse('articles-list'), success_data)
        self.assertEqual(responce.status_code, status.HTTP_201_CREATED)

    def test_retrieve(self):
        responce = self.client.get(reverse('articles-detail', kwargs={'pk': 1}))
        self.assertEqual(responce.status_code, status.HTTP_200_OK)

    def test_update(self):
        response = self.client.put(reverse('articles-detail', kwargs={'pk': 1}), success_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        response = self.client.post(reverse('articles-delete', kwargs={'pk': 1}), {'password': 'pass11'})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class FailTestCase(APITestCase):
    def setUp(self):
        hash_pass = PasswordHasher().hash('pass11')

        self.article = Article.objects.create(
            title='test',
            content='test',
            password=hash_pass
        )

    def test_create1(self):
        responce = self.client.post(reverse('articles-list'), fail_data1)
        self.assertNotEqual(responce.status_code, status.HTTP_201_CREATED)

    def test_create2(self):
        responce = self.client.post(reverse('articles-list'), fail_data2)
        self.assertNotEqual(responce.status_code, status.HTTP_201_CREATED)

    def test_create3(self):
        responce = self.client.post(reverse('articles-list'), fail_data3)
        self.assertNotEqual(responce.status_code, status.HTTP_201_CREATED)

    def test_retrieve(self):
        responce = self.client.get(reverse('articles-detail', kwargs={'pk': 2}))
        self.assertNotEqual(responce.status_code, status.HTTP_200_OK)

    def test_update1(self):
        response = self.client.put(reverse('articles-detail', kwargs={'pk': 1}), fail_data1)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_update2(self):
        response = self.client.put(reverse('articles-detail', kwargs={'pk': 1}), fail_data2)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_update3(self):
        response = self.client.put(reverse('articles-detail', kwargs={'pk': 1}), fail_data3)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        response = self.client.post(reverse('articles-delete', kwargs={'pk': 2}), {'password': 'pass11'})
        self.assertNotEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete(self):
        response = self.client.post(reverse('articles-delete', kwargs={'pk': 1}), {'password': 'pass22'})
        self.assertNotEqual(response.status_code, status.HTTP_204_NO_CONTENT)
