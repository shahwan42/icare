from django.shortcuts import reverse
from django.test import tag
from rest_framework.test import APITestCase, APIClient
from model_bakery import baker


@tag("user_ru")
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

    def test_user_detail_with_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user1.auth_token}")
        resp = self.client.get(self.url(self.user1.pk))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["name"], self.user1.name)
        self.assertEqual(resp.data["email"], self.user1.email)

    def test_user_detail_requires_authentication(self):
        resp = self.client.get(self.url(self.user1.pk))
        self.assertEqual(resp.status_code, 401)

    def test_user_detail_requires_same_user_only(self):
        self.client.force_authenticate(self.user1)
        resp = self.client.get(self.url(self.user2.pk))
        self.assertEqual(resp.status_code, 403)

    def test_update_user_details_put(self):
        self.client.force_authenticate(self.user1)
        payload = {
            "name": "Ahmed Shahwan",
            "email": "ahmed@shahwan.me",
            "password": "Awesome1",
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
        self.assertEqual(resp.status_code, 401)

        resp = self.client.patch(self.url(self.user1.pk), {"name": "New Name"})
        self.assertEqual(resp.status_code, 401)

    def test_update_user_details_same_user_only(self):
        self.client.force_authenticate(self.user1)
        resp = self.client.patch(self.url(self.user2.pk), {"name": "New Name"})
        self.assertEqual(resp.status_code, 403)


@tag("change_password")
class TestChangePassword(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("change_password")

        self.user = baker.make("users.CustomUser")
        self.user.set_password("Awesome1")
        self.user.save()

        self.payload = {
            "old_password": "Awesome1",
            "new_password": "Awesome2",
        }

    def test_change_password(self):
        self.assertTrue(self.user.check_password("Awesome1"))

        self.client.force_authenticate(self.user)
        resp = self.client.put(self.url, self.payload)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(self.user.check_password("Awesome2"))

    def test_change_password_requires_authentication(self):
        resp = self.client.put(self.url, self.payload)
        self.assertEqual(resp.status_code, 401)


@tag("auth_token")
class TestAuthToken(APITestCase):
    def setUp(self):
        self.user = baker.make("users.CustomUser")
        self.user.set_password("Awesome1")
        self.user.save()

        self.client = APIClient()
        self.url = reverse("auth_token")

    def test_login_creates_api_token(self):
        resp = self.client.post(
            self.url, {"username": self.user.email, "password": "Awesome1"}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("token", resp.data)


@tag("register")
class TestRegister(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("user_register")

    def test_register_desired_scenario(self):
        resp = self.client.post(
            self.url,
            {
                "email": "ahmed@shahwan.me",
                "password": "Awesome1",
                "name": "Ahmed Shahwan",
            },
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data["email"], "ahmed@shahwan.me")
        self.assertEqual(resp.data["name"], "Ahmed Shahwan")
        self.assertIn("token", resp.data)


@tag("logout")
class TestLogout(APITestCase):
    def setUp(self):
        self.user = baker.make("users.CustomUser")

        self.client = APIClient()
        self.url = reverse("user_logout")

    def test_logout_desired_scenario(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user.auth_token}")

        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)