from django.shortcuts import reverse
from django.test import tag
from rest_framework.test import APITestCase, APIClient
from model_bakery import baker


class TestUserRU(APITestCase):
    """Test User Retreive/Update/Partial Update"""

    def setUp(self):
        self.client = APIClient()
        self.user1 = baker.make("users.CustomUser")
        self.user2 = baker.make("users.CustomUser")

    def url(self, pk):
        return reverse("user_ru", args=[pk])

    def test_user_detail(self):
        self.client.force_authenticate(self.user1)
        resp = self.client.get(self.url(self.user1.pk))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["name"], self.user1.name)
        self.assertEqual(resp.data["email"], self.user1.email)

    def test_user_detail_requires_authentication(self):
        resp = self.client.get(self.url(self.user1.pk))
        self.assertEqual(resp.status_code, 403)

    def test_user_detail_requires_same_user_only(self):
        self.client.force_authenticate(self.user1)
        resp = self.client.get(self.url(self.user2.pk))
        self.assertEqual(resp.status_code, 403)

    def test_update_user_details_put(self):
        self.client.force_authenticate(self.user1)
        payload = {
            "name": "Ahmed Shahwan",
            "email": "ahmed@shahwan.me",
        }
        resp = self.client.put(self.url(self.user1.pk), payload)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["name"], "Ahmed Shahwan")
        self.assertEqual(resp.data["email"], "ahmed@shahwan.me")

    def test_update_user_details_patch(self):
        self.client.force_authenticate(self.user1)
        resp = self.client.patch(self.url(self.user1.pk), {"name": "New Name"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["name"], "New Name")
        self.assertEqual(resp.data["email"], self.user1.email)

    def test_update_user_details_requires_authentication(self):
        payload = {
            "name": "Ahmed Shahwan",
            "email": "ahmed@shahwan.me",
        }
        resp = self.client.put(self.url(self.user1.pk), payload)
        self.assertEqual(resp.status_code, 403)

        resp = self.client.patch(self.url(self.user1.pk), {"name": "New Name"})
        self.assertEqual(resp.status_code, 403)

    def test_update_user_details_same_user_only(self):
        self.client.force_authenticate(self.user1)
        resp = self.client.patch(self.url(self.user2.pk), {"name": "New Name"})
        self.assertEqual(resp.status_code, 403)


class TestChangePassword(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("change_password")

        self.user1 = baker.make("users.CustomUser")
        self.user1.set_password("Awesome1")
        self.user1.save()

        self.payload = {
            "old_password": "Awesome1",
            "new_password": "Awesome2",
        }

    def test_change_password(self):
        self.assertTrue(self.user1.check_password("Awesome1"))

        self.client.force_authenticate(self.user1)
        resp = self.client.put(self.url, self.payload)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(self.user1.check_password("Awesome2"))

    def test_change_password_requires_authentication(self):
        resp = self.client.put(self.url, self.payload)
        self.assertEqual(resp.status_code, 403)


class TestLogin(APITestCase):
    def setUp(self):
        pass

    def test_login_creates_api_token(self):
        pass
