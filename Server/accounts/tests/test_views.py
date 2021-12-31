from django.http import response
from django.test import Client, TestCase
from accounts.models import User
from accounts.tests.test_models import CreateUser, get_new_admin_user, get_new_user
from notes.tests.generic_functions import random_string
import string


class CreateCustomerViews(CreateUser):
    def __init__(self, username=None, email=None, password=None):
        CreateUser.__init__(self, username, email, password)
        self.client = Client()
        self.token = None

    def registration(self):
        """
        Registers a new uesr
        """
        self.check_user_exists()

        self.registration_resonse = self.client.post(
            path="/accounts/registration",
            data=dict(username=self.username, password=self.password),
        )

        # If login was valid, set the additional fields
        if self.registration_resonse.status_code == 200:
            # Update with the return token
            self.token = self.login_response.data["token"]
            # Update the self.client with the token header
            self.client = Client(HTTP_AUTHORIZATION=f"Token {self.token}")

    def login(self):
        """
        Log in the user
        """
        self.check_user_exists()

        self.login_response = self.client.post(
            path="/accounts/login",
            data=dict(username=self.username, password=self.password),
        )

        # If login was valid, set the additional fields
        if self.login_response.status_code == 200:
            # Update with the return token
            self.token = self.login_response.data["token"]
            # Update the self.client with the token header
            self.client = Client(HTTP_AUTHORIZATION=f"Token {self.token}")

    def logout(self):
        """
        Log out the user
        """
        self.logout_response = self.client.post(
            path="/accounts/logout", data=dict(token=self.token)
        )

    def logout_all(self):
        """
        Log out the user from all instances
        """
        self.logout_all_response = self.client.post(
            path="/accounts/logoutall", data=dict(token=self.token)
        )


def accounts_register(username, password):
    """
    Generic function to register a user
    """
    c = Client()
    return c.post("/accounts/registration", dict(username=username, password=password))


def accounts_login(username, password):
    """
    Generic function to login
    """
    c = Client()
    return c.post("/accounts/login", dict(username=username, password=password))


def user_token(admin=False, **user_info):
    """
    Returns a valid user token
    """
    if user_info:
        user = get_new_user(user_info)
    elif admin:
        user = get_new_admin_user()
    else:
        user = get_new_user()
    response = accounts_login(user["username"], user["password"])
    return response.data["token"]


def create_client(admin=False, **user_info):
    """
    Creates a client class with valid token for testing protected routes
    """
    token = user_token(admin, user_info)
    return Client(HTTP_AUTHORIZATION=f"Token {token}")


def accounts_logout(token):
    """
    Generic function to logout
    """
    c = create_client()
    return c.post("/accounts/logout")


def accounts_logoutall(token):
    """
    Generic function to logout
    """
    c = create_client()
    return c.post("/accounts/logoutall")


def make_post(as_admin=True, url=None, data=None, **user_info):
    """
    Function to quickly make a test post.

    Set admin status, the URL, and the data.
    """
    c = create_client(as_admin, user_info)
    return c.post(path=url, data=data, content_type="application/json")


def get_response(as_admin=True, url=None, data=None):
    """
    Function to quickly make a get request.

    Set admin status, the URL, and the (optional) data.
    """
    c = create_client(as_admin)
    return c.get(path=url, data=data)


class UserViewsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def setUp(self) -> None:
        return super().setUp()

    def test_user_log_in(self):
        """
        Test if the user can login successfully.
        Token of 64 chars should be returned on success.
        """
        user = get_new_user()
        response = accounts_login(user["username"], user["password"])
        self.assertEqual(response.status_code, 200, "Login status_code not 200")
        self.assertRegex(
            response.data["token"], "^[a-z0-9]{64}$", "Django knox token invalid regex"
        )
        self.assertRegex(
            response.data["expiry"],
            "^20\d{2}-[0-1]\d-[0-3]\dT[0-2]\d:[0-5]\d:\d{2}.\d{6}Z$",
            "Django knox invalid date format",
        )

    def test_user_bad_username(self):
        """
        Test a username not in the system fails out.
        """
        user = get_new_user()
        response = accounts_login("username_not_exist", user["password"])
        self.assertEqual(
            response.status_code,
            400,
            f"Bad username produced response status_code other than 400. Got {response.status_code}",
        )
        self.assertEqual(
            str(response.data["non_field_errors"][0]),
            "Unable to log in with provided credentials.",
            f"Unexpected response message. Got a message of '{str(response.data['non_field_errors'][0])}'",
        )
        self.assertEqual(
            response.data["non_field_errors"][0].code,
            "authorization",
            "Did not get the expected error code",
        )

    def test_user_bad_password(self):
        """
        Tests that a wrong password for a user fails out.
        """
        user = get_new_user()
        response = accounts_login(user["username"], "bad_password")
        self.assertEqual(
            response.status_code,
            400,
            f"Bad username produced response status_code other than 400. Got {response.status_code}",
        )
        self.assertEqual(
            str(response.data["non_field_errors"][0]),
            "Unable to log in with provided credentials.",
            f"Unexpected response message. Got a message of '{str(response.data['non_field_errors'][0])}'",
        )
        self.assertEqual(
            response.data["non_field_errors"][0].code,
            "authorization",
            "Did not get the expected error code",
        )

    def test_logout_success(self):
        """
        Tests that a user can properly logout.
        """
        user = get_new_user()
        response_login = accounts_login(user["username"], user["password"])
        # Ensure login was successful
        self.assertEqual(
            response_login.status_code,
            200,
            f"Login status_code not 200. Got a value of {response_login.status_code}",
        )
        # Get token
        token = response_login.data["token"]
        # Test that token is valid
        self.assertRegex(token, "^[a-z0-9]{64}$", "Django knox token invalid regex")
        # Get the logout response
        response_logout = accounts_logout(token)
        self.assertEqual(
            response_logout.status_code,
            204,
            f"Logout status_code not 204. Got a value of {response_logout.status_code}",
        )
        self.assertIsNone(
            response_logout.data,
            f"""Response contained unexpected messages:
        
        {response_logout.data}
        
        """,
        )

    def test_new_user_registration(self):
        """
        Tests the registration of a new user.
        """
        response = accounts_register(username="New_User", password="New_Password!")
        self.assertEqual(
            response.status_code,
            200,
            f"Login status_code not 200. Got a value of {response.status_code}",
        )
        self.assertRegex(
            response.data["token"], "^[a-z0-9]{64}$", "Django knox token invalid regex"
        )
        self.assertRegex(
            response.data["expiry"],
            "^20\d{2}-[0-1]\d-[0-3]\dT[0-2]\d:[0-5]\d:\d{2}.\d{6}Z$",
            "Django knox invalid date format",
        )

    def test_username_with_null_value(self):
        """
        Tests that a username with a null value can not be created.
        """
        response = accounts_register(
            username=f"name_with_{chr(0)}_symbol", password="Valid_Password!"
        )
        self.assertEqual(
            response.status_code,
            400,
            f"Accepted invalid null character with ordinal #0",
        )
        self.assertEqual(
            str(response.data["username"][0]),
            "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.",
            f"Unexpected error message on null username value. Got {str(response.data['username'][0])}",
        )
        self.assertEqual(
            str(response.data["username"][0].code),
            "invalid",
            f"Unexpected error code on null username value. Got {str(response.data['username'][0].code)}",
        )
        self.assertEqual(
            str(response.data["username"][1]),
            "Null characters are not allowed.",
            f"Unexpected error message on null username value. Got {str(response.data['username'][1])}",
        )
        self.assertEqual(
            str(response.data["username"][1].code),
            "null_characters_not_allowed",
            f"Unexpected error code on null username value. Got {str(response.data['username'][1].code)}",
        )

    def test_username_with_acceptable_and_unacceptable_characters(self):
        """
        Tests that a username with an unacceptable character can not be created.
        """
        acceptable_characters = string.ascii_letters + string.digits + "@.+-_"
        for value in range(1, 128):

            # Unacceptable character test
            if chr(value) not in acceptable_characters:
                response = accounts_register(
                    username=f"name_with_{chr(value)}_symbol",
                    password="Valid_Password!",
                )
                self.assertEqual(
                    response.status_code,
                    400,
                    f"Accepted invalid character {chr(value)} with ordinal #{value}",
                )
                self.assertEqual(
                    str(response.data["username"][0]),
                    "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.",
                    f"Unexpected error message on invalid username value. Got {str(response.data['username'][0])}",
                )
                self.assertEqual(
                    str(response.data["username"][0].code),
                    "invalid",
                    f"Unexpected error code on invalid username value. Got {str(response.data['username'][0].code)}",
                )

            # Acceptable character test
            if chr(value) in acceptable_characters:
                response = accounts_register(
                    username=f"name_with_{chr(value)}_symbol",
                    password="Valid_Password!",
                )
                self.assertEqual(
                    response.status_code,
                    200,
                    f"Did not accept valid character {chr(value)} with ordinal #{value}",
                )
                self.assertRegex(
                    response.data["token"],
                    "^[a-z0-9]{64}$",
                    "Django knox token invalid regex",
                )
                self.assertRegex(
                    response.data["expiry"],
                    "^20\d{2}-[0-1]\d-[0-3]\dT[0-2]\d:[0-5]\d:\d{2}.\d{6}Z$",
                    "Django knox invalid date format",
                )

    def test_password_with_null_value(self):
        """
        Tests that a password with a null value can not be created.
        """
        response = accounts_register(
            username="Valid_Username", password=f"password_with_{chr(0)}_symbol"
        )
        self.assertEqual(
            response.status_code,
            400,
            f"Accepted invalid null character with ordinal #0",
        )
        self.assertEqual(
            str(response.data["password"][0]),
            "Null characters are not allowed.",
            f"Unexpected error message on null password value. Got {str(response.data['password'][0])}",
        )
        self.assertEqual(
            str(response.data["password"][0].code),
            "null_characters_not_allowed",
            f"Unexpected error code on null password value. Got {str(response.data['password'][0].code)}",
        )

    def test_password_with_acceptable_characters(self):
        """
        Tests that a password with any symbol other than null can be created.
        """
        for value in range(1, 128):
            response = accounts_register(
                username=random_string(),
                password=f"password_with_{chr(value)}_symbol",
            )
            self.assertEqual(
                response.status_code,
                200,
                f"Accepted invalid character {chr(value)} with ordinal #{1}",
            )
            self.assertRegex(
                response.data["token"],
                "^[a-z0-9]{64}$",
                "Django knox token invalid regex",
            )
            self.assertRegex(
                response.data["expiry"],
                "^20\d{2}-[0-1]\d-[0-3]\dT[0-2]\d:[0-5]\d:\d{2}.\d{6}Z$",
                "Django knox invalid date format",
            )
