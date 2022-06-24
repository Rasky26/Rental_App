from accounts.tests.test_models import CreateUser
from django.test import Client, TestCase
import string


class CreateCustomerViews(CreateUser):
    def __init__(self, username=None, email=None, password=None):
        CreateUser.__init__(self, username, email, password)
        self.client = Client()
        self.token = None

    def make_async_client(self):
        """
        Overwrites client with AsyncClient() for async testing
        """
        # if not self.token:
        #     self.client=AsyncClient()

    def registration(self):
        """
        Registers a new uesr
        """
        self.registration_response = self.client.post(
            path="/accounts/registration",
            data=dict(username=self.username, password=self.password),
            content_type="application/json",
        )

        # If login was valid, set the additional fields
        if self.registration_response.status_code == 200:
            # Update with the return token
            self.token = self.registration_response.data["token"]
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
            content_type="application/json",
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
            path="/accounts/logout",
            data=dict(token=self.token),
            content_type="application/json",
        )

    def logout_all(self):
        """
        Log out the user from all instances
        """
        self.logout_all_response = self.client.post(
            path="/accounts/logoutall",
            data=dict(token=self.token),
            content_type="application/json",
        )


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
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        self.assertEqual(c.login_response.status_code, 200, "Login status_code not 200")
        self.assertIn("token", c.login_response.data, "Did not find expected key")
        self.assertRegex(c.token, "^[a-z0-9]{64}$", "Django knox token invalid regex")
        self.assertIn("expiry", c.login_response.data, "Did not find expected key")
        self.assertRegex(
            c.login_response.data["expiry"],
            "^20\d{2}-[0-1]\d-[0-3]\dT[0-2]\d:[0-5]\d:\d{2}.\d{6}Z$",
            "Django knox invalid date format",
        )

    def test_user_bad_username(self):
        """
        Test a username not in the system fails out.
        """
        c = CreateCustomerViews()
        c.create_user()
        c.username = "username_not_exist"
        c.login()

        self.assertEqual(
            c.login_response.status_code,
            400,
            f"Bad username produced response status_code other than 400. Got {c.login_response.status_code}",
        )
        self.assertEqual(
            c.login_response.data["non_field_errors"][0],
            "Unable to log in with provided credentials.",
            f"Unexpected response message. Got a message of '{c.login_response.data['non_field_errors'][0]}'",
        )
        self.assertEqual(
            c.login_response.data["non_field_errors"][0].code,
            "authorization",
            "Did not get the expected error code",
        )

    def test_user_bad_password(self):
        """
        Tests that a wrong password for a user fails out.
        """
        c = CreateCustomerViews()
        c.create_user()
        c.password = "bad_password"
        c.login()

        self.assertEqual(
            c.login_response.status_code,
            400,
            f"Bad username produced response status_code other than 400. Got {c.login_response.status_code}",
        )
        self.assertEqual(
            c.login_response.data["non_field_errors"][0],
            "Unable to log in with provided credentials.",
            f"Unexpected response message. Got a message of '{c.login_response.data['non_field_errors'][0]}'",
        )
        self.assertEqual(
            c.login_response.data["non_field_errors"][0].code,
            "authorization",
            "Did not get the expected error code",
        )

    def test_logout_success(self):
        """
        Tests that a user can properly logout.
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        # Ensure login was successful
        self.assertEqual(
            c.login_response.status_code,
            200,
            f"Login status_code not 200. Got a value of {c.login_response.status_code}",
        )
        # Test that token is valid
        self.assertRegex(c.token, "^[a-z0-9]{64}$", "Django knox token invalid regex")

        # Get the logout response
        c.logout()
        self.assertEqual(
            c.logout_response.status_code,
            204,
            f"Logout status_code not 204. Got a value of {c.logout_response.status_code}",
        )
        self.assertIsNone(
            c.logout_response.data,
            f"""Response contained unexpected messages:
        
        {c.logout_response.data}
        
        """,
        )

    def test_new_user_registration(self):
        """
        Tests the registration of a new user.
        """
        c = CreateCustomerViews(username="New_User", password="New_Password!")
        c.registration()

        self.assertEqual(
            c.registration_response.status_code,
            200,
            f"Login status_code not 200. Got a value of {c.registration_response.status_code}",
        )
        self.assertRegex(
            c.registration_response.data["token"],
            "^[a-z0-9]{64}$",
            "Django knox token invalid regex",
        )
        self.assertRegex(
            c.registration_response.data["expiry"],
            "^20\d{2}-[0-1]\d-[0-3]\dT[0-2]\d:[0-5]\d:\d{2}.\d{6}Z$",
            "Django knox invalid date format",
        )

    def test_username_with_null_value(self):
        """
        Tests that a username with a null value can not be created.
        """
        c = CreateCustomerViews(
            username=f"name_with_{chr(0)}_symbol", password="Valid_Password!"
        )
        c.registration()

        self.assertEqual(
            c.registration_response.status_code,
            400,
            f"Accepted invalid null character with ordinal #0",
        )
        self.assertIn(
            "registration-errors",
            c.registration_response.data,
            "Did not get expected key value",
        )
        self.assertIn(
            "username",
            c.registration_response.data["registration-errors"],
            "Did not get expected key value",
        )
        self.assertEqual(
            c.registration_response.data["registration-errors"]["username"][0],
            "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.",
            f"Unexpected error message on null username value. Got {c.registration_response.data['registration-errors']['username'][0]}",
        )
        self.assertEqual(
            c.registration_response.data["registration-errors"]["username"][0].code,
            "invalid",
            f"Unexpected error code on null username value. Got {c.registration_response.data['registration-errors']['username'][0].code}",
        )
        self.assertEqual(
            c.registration_response.data["registration-errors"]["username"][1],
            "Null characters are not allowed.",
            f"Unexpected error message on null username value. Got {c.registration_response.data['registration-errors']['username'][1]}",
        )
        self.assertEqual(
            c.registration_response.data["registration-errors"]["username"][1].code,
            "null_characters_not_allowed",
            f"Unexpected error code on null username value. Got {c.registration_response.data['registration-errors']['username'][1].code}",
        )

    def test_username_with_acceptable_and_unacceptable_characters(self):
        """
        Tests that a username with an unacceptable character can not be created.
        """
        c = CreateCustomerViews(password="Valid_Password!")

        acceptable_characters = string.ascii_letters + string.digits + "@.+-_"
        for value in range(1, 128):

            # Unacceptable character test
            if chr(value) not in acceptable_characters:
                c.username = f"name_with_{chr(value)}_symbol"
                c.registration()

                self.assertEqual(
                    c.registration_response.status_code,
                    400,
                    f"Accepted invalid character {chr(value)} with ordinal #{value}",
                )
                self.assertIn(
                    "registration-errors",
                    c.registration_response.data,
                    "Did not get expected key value",
                )
                self.assertIn(
                    "username",
                    c.registration_response.data["registration-errors"],
                    "Did not get expected key value",
                )
                self.assertEqual(
                    c.registration_response.data["registration-errors"]["username"][0],
                    "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.",
                    f"Unexpected error message on invalid username value. Got {c.registration_response.data['registration-errors']['username'][0]}",
                )
                self.assertEqual(
                    c.registration_response.data["registration-errors"]["username"][
                        0
                    ].code,
                    "invalid",
                    f"Unexpected error code on invalid username value. Got {c.registration_response.data['registration-errors']['username'][0].code}",
                )

            # Acceptable character test
            if chr(value) in acceptable_characters:
                c.username = f"name_with_{chr(value)}_symbol"
                c.registration()

                self.assertEqual(
                    c.registration_response.status_code,
                    200,
                    f"Did not accept valid character {chr(value)} with ordinal #{value}",
                )
                self.assertRegex(
                    c.registration_response.data["token"],
                    "^[a-z0-9]{64}$",
                    "Django knox token invalid regex",
                )
                self.assertRegex(
                    c.registration_response.data["expiry"],
                    "^20\d{2}-[0-1]\d-[0-3]\dT[0-2]\d:[0-5]\d:\d{2}.\d{6}Z$",
                    "Django knox invalid date format",
                )

    def test_password_with_null_value(self):
        """
        Tests that a password with a null value can not be created.
        """
        c = CreateCustomerViews(
            username="Valid_Username", password=f"password_with_{chr(0)}_symbol"
        )
        c.registration()

        self.assertEqual(
            c.registration_response.status_code,
            400,
            f"Accepted invalid null character with ordinal #0",
        )
        self.assertIn(
            "registration-errors",
            c.registration_response.data,
            "Did not get expected key value",
        )
        self.assertIn(
            "password",
            c.registration_response.data["registration-errors"],
            "Did not get expected key value",
        )
        self.assertEqual(
            c.registration_response.data["registration-errors"]["password"][0],
            "Null characters are not allowed.",
            f"Unexpected error message on null password value. Got {c.registration_response.data['registration-errors']['password'][0]}",
        )
        self.assertEqual(
            c.registration_response.data["registration-errors"]["password"][0].code,
            "null_characters_not_allowed",
            f"Unexpected error code on null password value. Got {c.registration_response.data['registration-errors']['password'][0].code}",
        )

    def test_password_with_acceptable_characters(self):
        """
        Tests that a password with any symbol other than null can be created.
        """
        c = CreateCustomerViews(username="Valid_Username")

        for value in range(1, 128):
            c.username = f"Valid_Username_{value}"
            c.password = f"password_with_{chr(value)}_symbol"
            c.registration()

            self.assertEqual(
                c.registration_response.status_code,
                200,
                f"Accepted invalid character {chr(value)} with ordinal #{1}",
            )
            self.assertIn(
                "token", c.registration_response.data, "Did not get expected key value"
            )
            self.assertRegex(
                c.registration_response.data["token"],
                "^[a-z0-9]{64}$",
                "Django knox token invalid regex",
            )
            self.assertIn(
                "expiry", c.registration_response.data, "Did not get expected key value"
            )
            self.assertRegex(
                c.registration_response.data["expiry"],
                "^20\d{2}-[0-1]\d-[0-3]\dT[0-2]\d:[0-5]\d:\d{2}.\d{6}Z$",
                "Django knox invalid date format",
            )

    # async def all_passwords_with_UTF8_chars_from_1_to_128(self):

    # https://docs.djangoproject.com/en/4.0/topics/testing/tools/#testing-asynchronous-code

    # c = CreateCustomerViews(username="Valid_Username")

    # for value in range(1, 128):
    #     c.username = f"Valid_Username_{value}"
    #     c.password = f"password_with_{chr(value)}_symbol"
    #     await c.registration()

    #     await self.assertEqual(
    #         c.registration_response.status_code,
    #         200,
    #         f"Accepted invalid character {chr(value)} with ordinal #{1}",
    #     )
    #     await self.assertIn(
    #         "token", c.registration_response.data, "Did not get expected key value"
    #     )
    #     await self.assertRegex(
    #         c.registration_response.data["token"],
    #         "^[a-z0-9]{64}$",
    #         "Django knox token invalid regex",
    #     )
    #     await self.assertIn(
    #         "expiry", c.registration_response.data, "Did not get expected key value"
    #     )
    #     await self.assertRegex(
    #         c.registration_response.data["expiry"],
    #         "^20\d{2}-[0-1]\d-[0-3]\dT[0-2]\d:[0-5]\d:\d{2}.\d{6}Z$",
    #         "Django knox invalid date format",
    #     )
