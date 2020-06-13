from django.test import TestCase
from django.contrib.auth import get_user_model


class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="normal@user.com", password="foo")
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser("super@user.com", "foo")
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False
            )

    def test_get_full_name_and_short_name(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="normal@user.com", password="foo", name="first last"
        )
        self.assertEqual(user.name, "first last")
        self.assertEqual(user.get_full_name(), "first last")
        self.assertEqual(user.get_short_name(), "first")

        another_user = User.objects.create_user(
            email="another_user@user.com", password="foo"
        )
        self.assertEqual(another_user.name, "")
        self.assertIsNone(another_user.get_full_name())
        self.assertIsNone(another_user.get_short_name())
