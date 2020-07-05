from unittest import skip
from django.test import tag
from django.shortcuts import reverse
from rest_framework.test import APIClient, APITestCase
from model_bakery import baker

from icare.core.models import List, Folder
from icare.users.models import CustomUser as User


@skip("Not needed for now")
@tag("lists")
class TestLists(APITestCase):
    def setUp(self) -> None:
        self.user = baker.make(User)

        self.folder = baker.make(Folder)

        self.list1 = baker.make(List, folder=self.folder, is_active=True)
        self.list2 = baker.make(List, folder=self.folder, is_active=True)
        self.list3 = baker.make(List, folder=self.folder)
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


@tag("folders")
class TestFolders(APITestCase):
    def setUp(self) -> None:
        self.user = baker.make(User)

        self.folder1 = baker.make(Folder, is_active=True)
        self.folder2 = baker.make(Folder, is_active=True)
        self.folder3 = baker.make(Folder, is_active=True)
        self.folder4 = baker.make(Folder)

        self.client = APIClient()
        self.url = reverse("core_folders")

    def test_get_all_folders(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 3)

    def test_get_folders_requires_authentication(self):
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(
            resp.json()["detail"], "Authentication credentials were not provided."
        )


@tag("folder")
class TestFolderDetail(APITestCase):
    def setUp(self) -> None:
        self.user = baker.make(User)

        self.folder = baker.make(Folder, is_active=True)
        self.list1 = baker.make(List, folder=self.folder, is_active=True)
        self.list2 = baker.make(List, folder=self.folder, is_active=True)
        self.list3 = baker.make(List, folder=self.folder)

        self.client = APIClient()

    def url_detail(self, pk):
        return reverse("core_folder", args=[pk])

    def test_getting_a_folder_requires_authentication(self):
        resp = self.client.get(self.url_detail(self.folder.pk))

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(
            resp.json()["detail"], "Authentication credentials were not provided."
        )

    def test_get_a_folder(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.url_detail(self.folder.pk))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json().get("id"), self.folder.id)
        self.assertEqual(resp.json().get("clickup_id"), self.folder.clickup_id)
        self.assertEqual(len(resp.json()["lists"]), 2)
