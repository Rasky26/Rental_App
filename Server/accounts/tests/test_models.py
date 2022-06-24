from django.test import TestCase
from accounts.models import User
from notes.tests.generic_functions import (
    random_bell_curve_int,
    random_string,
    random_length_string,
)


class CreateUser:
    """
    Class storing base user information
    """

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password
        self._random_user()

    def _random_user(self):
        """
        If all fields are None, set a random user information
        """
        if not any({self.username, self.email, self.password}):
            self.username = random_length_string(low=4, high=16)
            self.email = f"{self.username}@email.com"
            self.password = random_length_string(low=8, high=16)

    def create_user(self):
        """
        Creates a user in the database
        """
        self.user = User.objects.create_user(
            username=self.username, email=self.email, password=self.password
        )

    def check_user_exists(self):
        """
        Quickly check if the user exists. If not, create one
        """
        try:
            self.user
        except AttributeError:
            self.create_user()

    def create_or_set_admin(self):
        """
        Sets a user as an admin. If there is no user, create one.
        """
        self.check_user_exists()

        self.user.is_staff = True
        self.user.save()

    def set_name(self, first_name=None, last_name=None):
        """
        Sets the first and/or last name
        """
        self.check_user_exists()

        # Store the name values
        if first_name:
            self.first_name = first_name
            self.user.first_name = first_name
        if last_name:
            self.last_name = last_name
            self.user.last_name = last_name

        # Set name values to the User object
        self.user.save()


class UserModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def setUp(self):
        pass

    def test_user_return_string_only_username(self):
        """
        Create a user with only the username. User model should only return the username.
        """
        u = CreateUser(username="Test", email="test@email.com", password="password123!")
        u.create_user()

        user = User.objects.get(pk=u.user.id)

        self.assertEqual(user.username, "Test", "Did not get expected username")
        self.assertEqual(user.email, "test@email.com", "Did not get expected email")
        self.assertNotEqual(
            user.password,
            "password123!",
            "Password stored as plain text! FIX IMMEDIATELY!!!",
        )
        self.assertEqual(str(user), "Test", "User string was not matching")

    def test_user_return_string_username_first_name(self):
        """
        Create a user, then add a first_name. User model should return 'username | first_name'
        """
        u = CreateUser(username="Test", email="test@email.com", password="password123!")
        u.create_user()

        user = User.objects.get(pk=u.user.id)
        self.assertEqual(str(user), "Test", "Return string did not match username")

        u.set_name(first_name="John")
        user = User.objects.get(pk=u.user.id)
        self.assertEqual(str(user), "Test | John", "Bad user model string")

    def test_user_return_string_username_last_name(self):
        """
        Create a user, then add a last_name. User model should return 'username | last_name'
        """
        u = CreateUser(username="Test", email="test@email.com", password="password123!")
        u.create_user()

        user = User.objects.get(pk=u.user.id)
        self.assertEqual(str(user), "Test", "Return string did not match username")

        u.set_name(last_name="Doe")
        user = User.objects.get(pk=u.user.id)
        self.assertEqual(str(user), "Test | Doe", "Bad user model string")

    def test_user_return_string_username_full_name(self):
        """
        Create a user, then add a first and last name. User model should return 'username | first_name last_name'
        """
        u = CreateUser(username="Test", email="test@email.com", password="password123!")
        u.create_user()

        user = User.objects.get(pk=u.user.id)
        self.assertEqual(str(user), "Test", "Return string did not match username")

        u.set_name(first_name="John", last_name="Doe")
        user = User.objects.get(pk=u.user.id)
        self.assertEqual(str(user), "Test | John Doe", "Bad user model string")
