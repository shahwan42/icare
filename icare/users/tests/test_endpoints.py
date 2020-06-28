from django.shortcuts import reverse
from django.test import tag
from rest_framework.test import APITestCase, APIClient
from model_bakery import baker


class UserDetail(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = baker.make("users.CustomUser")
        self.user2 = baker.make("users.CustomUser")
        self.user3 = baker.make("users.CustomUser")

    def url_detail(self, pk):
        return reverse("user_ru", args=[pk])

    def test_user_detail(self):
        self.client.force_authenticate(self.user1)
        resp = self.client.get(reverse("user_ru", args=[self.user1.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["name"], self.user1.name)
        self.assertEqual(resp.data["email"], self.user1.email)

    def test_user_detail_requires_authentication(self):
        resp = self.client.get(reverse("user_ru", args=[self.user1.pk]))
        self.assertEqual(resp.status_code, 403)

    def test_user_detail_requires_same_user_only(self):
        self.client.force_authenticate(self.user1)
        resp = self.client.get(reverse("user_ru", args=[self.user2.pk]))
        self.assertEqual(resp.status_code, 403)

    def test_update_user_details(self):
        pass

    def test_update_user_details_requires_authentication(self):
        pass

    def test_update_user_details_same_user_only(self):
        pass

    def test_change_password(self):
        pass

    def test_change_password_requires_authentication(self):
        pass

    def test_change_password_same_user_only(self):
        pass
