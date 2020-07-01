from django.shortcuts import reverse
from rest_framework.test import APIClient, APITestCase
from model_bakery import baker

from icare.core.models import List, Folder
from icare.users.models import CustomUser as User


class TestLists(APITestCase):
    def setUp(self) -> None:
        self.user = baker.make(User)

        self.folder = baker.make(Folder)

        self.list1 = baker.make(List, folder=self.folder)
        self.list2 = baker.make(List, folder=self.folder)
        self.list3 = baker.make(List)

        self.client = APIClient()
        self.url = reverse("core_lists")

    def test_get_all_lists(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 3)

    def test_get_lists_requires_authentication(self):
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(
            resp.json()["detail"], "Authentication credentials were not provided."
        )
