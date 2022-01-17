from accounts.tests.test_models import CreateUser
from accounts.tests.test_views import CreateCustomerViews
from companies.models import CompanyInviteList
from companies.tests.test_models import create_company_invite, create_company_obj
from contacts.tests.test_views import get_address_data, get_contact_data
from core.settings import BASE_DIR
from datetime import datetime, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.utils import timezone
from os import listdir
from os import remove as os_remove
from os.path import join as os_join
from notes.tests.generic_functions import (
    random_bell_curve_int,
    random_string,
    random_sentence,
)
from unittest import mock
import pytz
import string

# import tempfile
from pprint import pprint
import json


def company_data(
    name=None, random_address=True, random_contact=True, num_contacts=2, num_notes=2
):
    """
    Return data JSON to quickly create a company
    """
    if not name:
        name = random_string(text=string.ascii_letters).title()

    return dict(
        business_name=name,
        legal_name=f"{name} LLC",
        business_address=get_address_data(random_address),
        mailing_address=get_address_data(random_address),
        contacts=[get_contact_data(random_contact) for _ in range(num_contacts)],
        notes=[
            dict(note=random_sentence(total_len=random_bell_curve_int(low=1, high=128)))
            for _ in range(num_notes)
        ],
    )


class CompaniesViewsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def setUp(self):
        pass

    def test_company_creation(self):
        """
        Creates a company and properly assigns the current user as admin
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        res = c.client.post(
            path="/companies/create",
            data=company_data(
                name="Test Company",
                random_address=False,
                random_contact=False,
                num_contacts=5,
            ),
            content_type="application/json",
        )

        self.assertEqual(
            res.status_code, 201, f"Expected 201 status code. Got {res.status_code}"
        )
        self.assertEqual(
            res.data["business_name"],
            "Test Company",
            "Did not get the correct business name",
        )
        self.assertEqual(
            res.data["legal_name"],
            "Test Company LLC",
            "Did not get the correct legal name",
        )
        self.assertEqual(
            f"{res.data['business_address']['address_1']} {res.data['business_address']['address_2']} {res.data['business_address']['city']} {res.data['business_address']['state']} {res.data['business_address']['zipcode']}",
            "111 1st St. S Apt. 1 City MN 55555-5555",
            "Did not get the correct business address",
        )
        self.assertEqual(
            f"{res.data['mailing_address']['address_1']} {res.data['mailing_address']['address_2']} {res.data['mailing_address']['city']} {res.data['mailing_address']['state']} {res.data['mailing_address']['zipcode']}",
            "111 1st St. S Apt. 1 City MN 55555-5555",
            "Did not get the correct mailing address",
        )
        self.assertEqual(
            len(res.data["contacts"]),
            5,
            f"Expected 5 contacts. Got {len(res.data['contacts'])}",
        )
        for contact in res.data["contacts"]:
            self.assertEqual(
                f"{contact['name_prefix']} {contact['name_first']} {contact['name_middle']} {contact['name_last']} {contact['name_suffix']} {contact['phone_1']} {contact['phone_2']} {contact['email']}",
                "Mr. John E Doe Esq. 1234567890 9876543210 john@email.com",
                "Did not get the expected contact information",
            )
        self.assertEqual(
            res.data["gl_code"]["name"],
            "Test Company",
            "Wrong company general ledger name",
        )
        self.assertFalse(res.data["gl_code"]["code"], "Company gl code not empty")
        self.assertEqual(
            res.data["gl_code"]["description"],
            "Test Company general ledger",
            "Automatic company gl description does not match",
        )
        self.assertFalse(
            res.data["gl_code"]["notes"],
            "Notes for automatically created company general ledger account should have been blank",
        )
        self.assertEqual(
            res.data["accounts_payable_gl"]["name"],
            "Accounts Payable",
            "Automatic name for accounts payable gl wrong",
        )
        self.assertFalse(
            res.data["accounts_payable_gl"]["code"],
            "Accounts payable gl code not empty",
        )
        self.assertEqual(
            res.data["accounts_payable_gl"]["description"],
            "Accounts Payable ledger for Test Company",
            "Automatic company accounts payable gl description does not match",
        )
        self.assertFalse(
            res.data["accounts_payable_gl"]["notes"],
            "Notes for automatically created accounts payable general ledger account should have been blank",
        )
        self.assertEqual(
            res.data["accounts_receivable_gl"]["name"],
            "Accounts Receivable",
            "Automatic name for accounts receivable gl wrong",
        )
        self.assertFalse(
            res.data["accounts_receivable_gl"]["code"],
            "Accounts receivable gl code not empty",
        )
        self.assertEqual(
            res.data["accounts_receivable_gl"]["description"],
            "Accounts Receivable ledger for Test Company",
            "Automatic company accounts receivable gl description does not match",
        )
        self.assertFalse(
            res.data["accounts_receivable_gl"]["notes"],
            "Notes for automatically created accounts receivable general ledger account should have been blank",
        )
        self.assertEqual(
            len(res.data["allowed_admins"]),
            1,
            f"Expected 1 allowed_admin. Got {len(res.data['allowed_admins'])}",
        )
        self.assertEqual(
            res.data["allowed_admins"][0]["username"],
            c.username,
            "Registering user not set as allowed_admin",
        )
        self.assertFalse(
            res.data["allowed_viewers"], "Did not get an empty allowed_viewers list"
        )
        self.assertEqual(
            len(res.data["notes"]), 2, f"Expected 2 notes. Got {len(res.data['notes'])}"
        )
        self.assertFalse(
            res.data["accounts_payable_extension"],
            "Accounts payable expansion not False",
        )
        self.assertFalse(
            res.data["accounts_receivable_extension"],
            "Accounts receivable expansion not False",
        )
        self.assertFalse(
            res.data["maintenance_extension"], "Maintenance expansion not False"
        )

    def test_company_creation_with_no_address_information(self):
        """
        Tests that no address is created if no information is passed. Test one address as null and the other full of blanks
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        data = company_data(num_contacts=0, num_notes=0)
        data["business_address"] = None
        data["mailing_address"] = dict(
            address_1="", address_2="", city="", state="", zipcode=""
        )

        res = c.client.post(
            path="/companies/create", data=data, content_type="application/json"
        )

        self.assertEqual(
            res.status_code, 201, f"Expected 201 status code. Got {res.status_code}"
        )
        self.assertIsNone(res.data["business_address"], "Business address was not None")
        self.assertIsNone(res.data["mailing_address"], "Mailing address was not None")

    def test_company_create_with_partial_address_information(self):
        """
        Ensures the address data is upheld as passed
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        data = company_data(num_contacts=0, num_notes=0)
        data["business_address"] = None
        data["mailing_address"] = dict(
            address_1="111 1st St. S", address_2="", city="", state="", zipcode=""
        )
        res = c.client.post(
            path="/companies/create", data=data, content_type="application/json"
        )

        self.assertEqual(
            res.status_code, 201, f"Expected 201 status code. Got {res.status_code}"
        )
        self.assertIsNone(res.data["business_address"], "Business address was not None")

        m = res.data["mailing_address"]
        self.assertEqual(
            f"{m['address_1']}{m['address_2']}{m['city']}{m['state']}{m['zipcode']}",
            "111 1st St. S",
            "Did not get expected mailing address",
        )

    def test_non_authenticated_user_can_not_create_company(self):
        """
        Ensures that a non-authenticated user can not create a company
        """
        c = Client()
        res = c.post(
            path="/companies/create",
            data=company_data(),
            content_type="application/json",
        )

        self.assertEqual(
            res.status_code, 401, f"Expected 401 status code. Got {res.status_code}"
        )
        self.assertTrue("detail" in res.data, "'detail' not in response dict")
        self.assertEqual(
            str(res.data["detail"]),
            "Authentication credentials were not provided.",
            "Did not get the expected error message",
        )
        self.assertEqual(
            res.data["detail"].code,
            "not_authenticated",
            "Did not receive the correct error code",
        )


class CompaniesInviteListTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def setUp(self):
        pass

    def test_removal_expired_invites(self):
        """
        Ensures all records of expired invites are deleted
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        company = create_company_obj()
        company.allowed_admins.add(c.user)

        # Set outdated timestamp
        mocked = datetime(2021, 12, 1, 0, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            # Create first invite
            create_company_invite(
                email="test_1@email.com", admin_in=True, viewer_in=False
            )

        # Set another outdated timestamp
        mocked = datetime.now(tz=pytz.utc) - timedelta(days=7, minutes=1)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            # Create second invite
            create_company_invite(email="test_2@email.com")

        # Set a valid timestamp
        mocked = datetime.now(tz=pytz.utc) - timedelta(days=6, hours=23, minutes=59)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            # Create second invite
            create_company_invite(email="test_3@email.com")

        # Get invites queryset
        invites = CompanyInviteList.objects.all()

        self.assertEqual(len(invites), 3, f"Expected 3 invites, Got {len(invites)}")
        for invite in invites:
            if invite.id in [1, 2]:
                # Check that invites have expected start dates
                self.assertLess(
                    invite.updated_at + timedelta(days=7),
                    timezone.now(),
                    "Check test object start date if more than 7 days before now",
                )
                # Check the timeout status
                self.assertTrue(
                    invite.timeout,
                    "Check model timeout date of seven (7) days",
                )
            else:
                # Check that invites have expected start dates
                self.assertGreater(
                    invite.updated_at + timedelta(days=7),
                    timezone.now(),
                    "Check test object start date if more than 7 days before now",
                )
                # Check the timeout status
                self.assertFalse(
                    invite.timeout,
                    "Check model timeout date of seven (7) days",
                )

        res = c.client.post(
            path=f"/companies/invite/{company.id}",
            data=dict(email="test@email.com", admin_in=True, viewer_in=False),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 201, f"Expected 201. Got {res.status_code}")

        # Get updated invites queryset
        invites = CompanyInviteList.objects.all()

        self.assertEqual(len(invites), 2, f"Expected 2 invites, Got {len(invites)}")

        for invite in invites:
            self.assertFalse(invite.timeout, "Timeout was not False")
            self.assertGreaterEqual(
                invite.updated_at,
                timezone.now() - timedelta(days=7),
                "Remaining invite not meeting time criterium. Check the model timeout amount",
            )

    def test_invite_for_non_existant_company(self):
        """
        Verifies response when a non-existant company invite is sent
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        res = c.client.post(
            path="/companies/invite/1234",
            data=dict(email="test@email.com", admin_in=True, viewer_in=False),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 400, f"Expected 400. Got {res.status_code}")
        self.assertIn("invite-error", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["invite-error"],
            "invalid invite permissions for requested company",
            "Custom message did not match",
        )
        self.assertIn("detail", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["detail"],
            "Can not invite user to company with ID 1234",
            "Custom message did not match",
        )

    def test_invite_to_company_without_proper_allowed_admin_permission(self):
        """
        Verifies response when a non-existant company invite is sent
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        company = create_company_obj()

        res = c.client.post(
            path=f"/companies/invite/{company.id}",
            data=dict(email="test@email.com", admin_in=True, viewer_in=False),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 400, f"Expected 400. Got {res.status_code}")
        self.assertIn("invite-error", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["invite-error"],
            "invalid invite permissions for requested company",
            "Custom message did not match",
        )
        self.assertIn("detail", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["detail"],
            "Can not invite user to company with ID 1",
            "Custom message did not match",
        )

    def test_invite_to_company_where_no_permission_level_is_specified(self):
        """
        Verifies response when a non-existant company invite is sent
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        company = create_company_obj()
        company.allowed_admins.add(c.user)

        # Set admin_in AND viewer_in both to FALSE
        res = c.client.post(
            path=f"/companies/invite/{company.id}",
            data=dict(email="test@email.com", admin_in=False, viewer_in=False),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 400, f"Expected 400. Got {res.status_code}")
        self.assertIn("invalid-invite", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["invalid-invite"],
            "clashing permission levels specified",
            "Custom message did not match",
        )
        self.assertIn("invalid-info", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["invalid-info"],
            "admin_in was 'False' & viewer_in was 'False'",
            "Custom message did not match",
        )

    def test_invite_to_company_where_both_permission_levels_are_specified(self):
        """
        Verifies response when a non-existant company invite is sent
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        company = create_company_obj()
        company.allowed_admins.add(c.user)

        # Set admin_in AND viewer_in both to TRUE
        res = c.client.post(
            path=f"/companies/invite/{company.id}",
            data=dict(email="test@email.com", admin_in=True, viewer_in=True),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 400, f"Expected 400. Got {res.status_code}")
        self.assertIn("invalid-invite", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["invalid-invite"],
            "clashing permission levels specified",
            "Custom message did not match",
        )
        self.assertIn("invalid-info", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["invalid-info"],
            "admin_in was 'True' & viewer_in was 'True'",
            "Custom message did not match",
        )

    def test_serializer_fails_on_invalid_email(self):
        """
        Verifies response when a non-existant company invite is sent
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        company = create_company_obj()
        company.allowed_admins.add(c.user)

        # Set admin_in AND viewer_in both to TRUE
        res = c.client.post(
            path=f"/companies/invite/{company.id}",
            data=dict(email="test@email", admin_in=True, viewer_in=False),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 400, f"Expected 400. Got {res.status_code}")
        self.assertIn("invite-error", res.data, "Did not find expected key")
        self.assertIn("email", res.data["invite-error"], "Did not find expected key")
        self.assertEqual(
            res.data["invite-error"]["email"][0],
            "Enter a valid email address.",
            "Invalid email address not matching",
        )
        self.assertEqual(
            res.data["invite-error"]["email"][0].code,
            "invalid",
            "Invalid email address code not matching",
        )

    def test_company_admin_invite_new_user_as_viewer(self):
        """
        Creates admin invite to company
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        # Set outdated timestamp
        mocked = datetime(2021, 12, 1, 0, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):

            company = create_company_obj(random_info=False)
            company.allowed_admins.add(c.user)

            data = dict(email="test@email.com", admin_in=False, viewer_in=True)

            res = c.client.post(
                path=f"/companies/invite/{company.id}",
                data=data,
                content_type="application/json",
            )

        self.assertEqual(res.status_code, 201, f"Expected 201. Got {res.status_code}")
        self.assertIn("email", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["email"], "test@email.com", "Did not get the expected email"
        )
        self.assertIn("admin_in", res.data, "Did not find expected key")
        self.assertIsNone(res.data["admin_in"], "admin_in was not None")
        self.assertIn("viewer_in", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["viewer_in"]["company_name"],
            "Test | Test LLC",
            "viewer_in invite id not matching expected company id",
        )
        self.assertIn("valid_until", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["valid_until"],
            "Dec. 08, 2021 - 12:00 AM UTC",
            "Did not get the correct valid time",
        )

    def test_company_admin_invite_new_user_as_admin(self):
        """
        Creates admin invite to company
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        # Set outdated timestamp
        mocked = datetime(2021, 12, 1, 0, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):

            company = create_company_obj(random_info=False)
            company.allowed_admins.add(c.user)

            data = dict(email="test@email.com", admin_in=True, viewer_in=False)

            res = c.client.post(
                path=f"/companies/invite/{company.id}",
                data=data,
                content_type="application/json",
            )

        self.assertEqual(res.status_code, 201, f"Expected 201. Got {res.status_code}")
        self.assertIn("email", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["email"], "test@email.com", "Did not get the expected email"
        )
        self.assertIn("admin_in", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["admin_in"]["company_name"],
            "Test | Test LLC",
            "admin_in invite id not matching expected company id",
        )
        self.assertIn("viewer_in", res.data, "Did not find expected key")
        self.assertIsNone(res.data["viewer_in"], "viewer_in was not None")
        self.assertIn("valid_until", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["valid_until"],
            "Dec. 08, 2021 - 12:00 AM UTC",
            "Did not get the correct valid time",
        )

    def test_company_admin_invite_new_user_as_admin_when_they_are_already_pending_as_viewer(
        self,
    ):
        """
        Creates admin invite to company
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        # Set specific timestamp
        mocked = datetime(2021, 12, 1, 0, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):

            company = create_company_obj(random_info=False)
            company.allowed_admins.add(c.user)

            invite = create_company_invite(
                company_obj=company,
                email="test@email.com",
                admin_in=False,
                viewer_in=True,
            )

        self.assertEqual(company.id, 1, "Company ID did not get expected value of 1")
        self.assertEqual(invite.email, "test@email.com", "wrong email")
        self.assertIsNone(invite.admin_in, "admin_in not None")
        self.assertEqual(
            invite.viewer_in, company, "viewer_in not assigned to correct company"
        )
        self.assertTrue(invite.timeout, "should have timed out long ago")

        # Set updated timestamp
        mocked = datetime(2021, 12, 5, 0, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):

            data = dict(email="test@email.com", admin_in=True, viewer_in=False)

            res = c.client.post(
                path=f"/companies/invite/{company.id}",
                data=data,
                content_type="application/json",
            )

        self.assertEqual(res.status_code, 201, f"Expected 201. Got {res.status_code}")
        self.assertIn("email", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["email"], "test@email.com", "Did not get the expected email"
        )
        self.assertIn("admin_in", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["admin_in"]["company_name"],
            "Test | Test LLC",
            "admin_in invite id not matching expected company id",
        )
        self.assertIn("viewer_in", res.data, "Did not find expected key")
        self.assertIsNone(res.data["viewer_in"], "viewer_in was not None")
        self.assertIn("valid_until", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["valid_until"],
            "Dec. 12, 2021 - 12:00 AM UTC",
            "Did not get the correct valid time",
        )

    def test_company_admin_invite_new_user_as_admin_when_they_are_already_pending_as_admin(
        self,
    ):
        """
        Creates admin invite to company
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        # Set specific timestamp
        mocked = datetime(2021, 12, 1, 0, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):

            company = create_company_obj(random_info=False)
            company.allowed_admins.add(c.user)

            invite = create_company_invite(
                company_obj=company,
                email="test@email.com",
                admin_in=True,
                viewer_in=False,
            )

        self.assertEqual(company.id, 1, "Company ID did not get expected value of 1")
        self.assertEqual(invite.email, "test@email.com", "wrong email")
        self.assertEqual(
            invite.admin_in, company, "admin_in not assigned to correct company"
        )
        self.assertIsNone(invite.viewer_in, "viewer_in not None")
        self.assertTrue(invite.timeout, "should have timed out long ago")

        # Set updated timestamp
        mocked = datetime(2021, 12, 5, 0, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):

            data = dict(email="test@email.com", admin_in=True, viewer_in=False)

            res = c.client.post(
                path=f"/companies/invite/{company.id}",
                data=data,
                content_type="application/json",
            )

        self.assertEqual(res.status_code, 201, f"Expected 201. Got {res.status_code}")
        self.assertIn("email", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["email"], "test@email.com", "Did not get the expected email"
        )
        self.assertIn("admin_in", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["admin_in"]["company_name"],
            "Test | Test LLC",
            "admin_in invite id not matching expected company id",
        )
        self.assertIn("viewer_in", res.data, "Did not find expected key")
        self.assertIsNone(res.data["viewer_in"], "viewer_in was not None")
        self.assertIn("valid_until", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["valid_until"],
            "Dec. 12, 2021 - 12:00 AM UTC",
            "Did not get the correct valid time",
        )

    def test_company_admin_invite_new_user_as_viewer_when_they_are_already_pending_as_admin(
        self,
    ):
        """
        Creates admin invite to company
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        # Set specific timestamp
        mocked = datetime(2021, 12, 1, 0, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):

            company = create_company_obj(random_info=False)
            company.allowed_admins.add(c.user)

            invite = create_company_invite(
                company_obj=company,
                email="test@email.com",
                admin_in=True,
                viewer_in=False,
            )

        self.assertEqual(company.id, 1, "Company ID did not get expected value of 1")
        self.assertEqual(invite.email, "test@email.com", "wrong email")
        self.assertEqual(
            invite.admin_in, company, "admin_in not assigned to correct company"
        )
        self.assertIsNone(invite.viewer_in, "viewer_in not None")
        self.assertTrue(invite.timeout, "should have timed out long ago")

        # Set updated timestamp
        mocked = datetime(2021, 12, 5, 0, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):

            data = dict(email="test@email.com", admin_in=False, viewer_in=True)

            res = c.client.post(
                path=f"/companies/invite/{company.id}",
                data=data,
                content_type="application/json",
            )

        self.assertEqual(res.status_code, 201, f"Expected 201. Got {res.status_code}")
        self.assertIn("email", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["email"], "test@email.com", "Did not get the expected email"
        )
        self.assertIn("admin_in", res.data, "Did not find expected key")
        self.assertIsNone(res.data["admin_in"], "admin_in was not None")
        self.assertIn("viewer_in", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["viewer_in"]["company_name"],
            "Test | Test LLC",
            "viewer_in invite id not matching expected company id",
        )
        self.assertIn("valid_until", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["valid_until"],
            "Dec. 12, 2021 - 12:00 AM UTC",
            "Did not get the correct valid time",
        )

    def test_company_admin_invite_new_user_as_viewer_when_they_are_already_pending_as_viewer(
        self,
    ):
        """
        Creates admin invite to company
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        # Set specific timestamp
        mocked = datetime(2021, 12, 1, 0, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):

            company = create_company_obj(random_info=False)
            company.allowed_admins.add(c.user)

            invite = create_company_invite(
                company_obj=company,
                email="test@email.com",
                admin_in=False,
                viewer_in=True,
            )

        self.assertEqual(company.id, 1, "Company ID did not get expected value of 1")
        self.assertEqual(invite.email, "test@email.com", "wrong email")
        self.assertIsNone(invite.admin_in, "admin_in not None")
        self.assertEqual(
            invite.viewer_in, company, "viewer_in not assigned to correct company"
        )
        self.assertTrue(invite.timeout, "should have timed out long ago")

        # Set updated timestamp
        mocked = datetime(2021, 12, 5, 0, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):

            data = dict(email="test@email.com", admin_in=False, viewer_in=True)

            res = c.client.post(
                path=f"/companies/invite/{company.id}",
                data=data,
                content_type="application/json",
            )

        self.assertEqual(res.status_code, 201, f"Expected 201. Got {res.status_code}")
        self.assertIn("email", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["email"], "test@email.com", "Did not get the expected email"
        )
        self.assertIn("admin_in", res.data, "Did not find expected key")
        self.assertIsNone(res.data["admin_in"], "admin_in was not None")
        self.assertIn("viewer_in", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["viewer_in"]["company_name"],
            "Test | Test LLC",
            "viewer_in invite id not matching expected company id",
        )
        self.assertIn("valid_until", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["valid_until"],
            "Dec. 12, 2021 - 12:00 AM UTC",
            "Did not get the correct valid time",
        )

    def test_company_admin_invite_new_user_with_duplicate_invites_already_in_the_model(
        self,
    ):
        """
        Creates admin invite to company
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        # Set specific timestamp
        mocked = datetime(2021, 12, 1, 0, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):

            company = create_company_obj(random_info=False)
            company.allowed_admins.add(c.user)

            invite_1 = create_company_invite(
                company_obj=company,
                email="test@email.com",
                admin_in=False,
                viewer_in=True,
            )

            invite_2 = create_company_invite(
                company_obj=company,
                email="test@email.com",
                admin_in=False,
                viewer_in=True,
            )

        self.assertEqual(company.id, 1, "Company ID did not get expected value of 1")
        self.assertEqual(invite_1.email, "test@email.com", "wrong email")
        self.assertIsNone(invite_1.admin_in, "admin_in not None")
        self.assertEqual(
            invite_1.viewer_in, company, "viewer_in not assigned to correct company"
        )
        self.assertTrue(invite_1.timeout, "should have timed out long ago")
        self.assertEqual(invite_2.email, "test@email.com", "wrong email")
        self.assertIsNone(invite_2.admin_in, "admin_in not None")
        self.assertEqual(
            invite_2.viewer_in, company, "viewer_in not assigned to correct company"
        )
        self.assertTrue(invite_2.timeout, "should have timed out long ago")

        # Set updated timestamp
        mocked = datetime(2021, 12, 5, 0, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):

            data = dict(email="test@email.com", admin_in=False, viewer_in=True)

            res = c.client.post(
                path=f"/companies/invite/{company.id}",
                data=data,
                content_type="application/json",
            )

        self.assertEqual(res.status_code, 201, f"Expected 201. Got {res.status_code}")
        self.assertIn("email", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["email"], "test@email.com", "Did not get the expected email"
        )
        self.assertIn("admin_in", res.data, "Did not find expected key")
        self.assertIsNone(res.data["admin_in"], "admin_in was not None")
        self.assertIn("viewer_in", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["viewer_in"]["company_name"],
            "Test | Test LLC",
            "viewer_in invite id not matching expected company id",
        )
        self.assertIn("valid_until", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["valid_until"],
            "Dec. 12, 2021 - 12:00 AM UTC",
            "Did not get the correct valid time",
        )

    def test_company_admin_invite_for_existing_user_not_associated_with_current_company(
        self,
    ):
        """
        Creates admin invite to company
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        invite_user = CreateUser(
            username="Test", email="test@email.com", password="123456789"
        )
        invite_user.create_user()

        company = create_company_obj(random_info=False)
        company.allowed_admins.add(c.user)

        data = dict(email="test@email.com", admin_in=False, viewer_in=True)

        # Set updated timestamp
        mocked = datetime(2021, 12, 5, 0, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):

            res = c.client.post(
                path=f"/companies/invite/{company.id}",
                data=data,
                content_type="application/json",
            )

        self.assertEqual(res.status_code, 201, f"Expected 201. Got {res.status_code}")
        self.assertIn("email", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["email"], "test@email.com", "Did not get the expected email"
        )
        self.assertIn("admin_in", res.data, "Did not find expected key")
        self.assertIsNone(res.data["admin_in"], "admin_in was not None")
        self.assertIn("viewer_in", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["viewer_in"]["company_name"],
            "Test | Test LLC",
            "viewer_in invite id not matching expected company id",
        )
        self.assertIn("valid_until", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["valid_until"],
            "Dec. 12, 2021 - 12:00 AM UTC",
            "Did not get the correct valid time",
        )

    def test_company_admin_invite_for_existing_admin_user_already_associated_with_current_company(
        self,
    ):
        """
        Creates admin invite to company
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        invite_user = CreateUser(
            username="Test", email="test@email.com", password="123456789"
        )
        invite_user.create_user()

        company = create_company_obj(random_info=False)
        company.allowed_admins.add(c.user, invite_user.user)

        data = dict(email="test@email.com", admin_in=True, viewer_in=False)

        # Set updated timestamp
        mocked = datetime(2021, 12, 5, 0, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):

            res = c.client.post(
                path=f"/companies/invite/{company.id}",
                data=data,
                content_type="application/json",
            )

        self.assertEqual(res.status_code, 200, f"Expected 200. Got {res.status_code}")
        self.assertIn("existing-admin", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["existing-admin"],
            "Requested user with email 'test@email.com' is already set as an admin for 'Test | Test LLC'",
            "Did not get the expected email",
        )
        self.assertIn("existing-email", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["existing-email"],
            "test@email.com",
            "Did not receive expected email",
        )

    def test_company_admin_invite_for_existing_viewer_user_already_associated_with_current_company(
        self,
    ):
        """
        Creates admin invite to company
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        invite_user = CreateUser(
            username="Test", email="test@email.com", password="123456789"
        )
        invite_user.create_user()

        company = create_company_obj(random_info=False)
        company.allowed_admins.add(c.user)
        company.allowed_viewers.add(invite_user.user)

        data = dict(email="test@email.com", admin_in=True, viewer_in=False)

        # Set updated timestamp
        mocked = datetime(2021, 12, 5, 0, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):

            res = c.client.post(
                path=f"/companies/invite/{company.id}",
                data=data,
                content_type="application/json",
            )

        self.assertEqual(res.status_code, 200, f"Expected 200. Got {res.status_code}")
        self.assertIn("existing-viewer", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["existing-viewer"],
            "Requested user with email 'test@email.com' is already set as a viewer for 'Test | Test LLC'",
            "Did not get the expected email",
        )
        self.assertIn("existing-email", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["existing-email"],
            "test@email.com",
            "Did not receive expected email",
        )
        self.assertIn("no-change", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["no-change"],
            "Viewer status unchanged. Change permission levels in the company parameters.",
            "Did not receive expected email",
        )

    def test_company_viewer_invite_for_existing_admin_user_already_associated_with_current_company(
        self,
    ):
        """
        Creates admin invite to company
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        invite_user = CreateUser(
            username="Test", email="test@email.com", password="123456789"
        )
        invite_user.create_user()

        company = create_company_obj(random_info=False)
        company.allowed_admins.add(c.user, invite_user.user)

        data = dict(email="test@email.com", admin_in=False, viewer_in=True)

        # Set updated timestamp
        mocked = datetime(2021, 12, 5, 0, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):

            res = c.client.post(
                path=f"/companies/invite/{company.id}",
                data=data,
                content_type="application/json",
            )

        self.assertEqual(res.status_code, 200, f"Expected 200. Got {res.status_code}")
        self.assertIn("existing-admin", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["existing-admin"],
            "Requested user with email 'test@email.com' is already set as an admin for 'Test | Test LLC'",
            "Did not get the expected email",
        )
        self.assertIn("existing-email", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["existing-email"],
            "test@email.com",
            "Did not receive expected email",
        )
        self.assertIn("no-change", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["no-change"],
            "Admin status unchanged. Change permission levels in the company parameters.",
            "Did not receive expected email",
        )

    def test_company_viewer_invite_for_existing_viewer_user_already_associated_with_current_company(
        self,
    ):
        """
        Creates admin invite to company
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        invite_user = CreateUser(
            username="Test", email="test@email.com", password="123456789"
        )
        invite_user.create_user()

        company = create_company_obj(random_info=False)
        company.allowed_admins.add(c.user)
        company.allowed_viewers.add(invite_user.user)

        data = dict(email="test@email.com", admin_in=False, viewer_in=True)

        # Set updated timestamp
        mocked = datetime(2021, 12, 5, 0, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):

            res = c.client.post(
                path=f"/companies/invite/{company.id}",
                data=data,
                content_type="application/json",
            )

        self.assertEqual(res.status_code, 200, f"Expected 200. Got {res.status_code}")
        self.assertIn("existing-viewer", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["existing-viewer"],
            "Requested user with email 'test@email.com' is already set as a viewer for 'Test | Test LLC'",
            "Did not get the expected email",
        )
        self.assertIn("existing-email", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["existing-email"],
            "test@email.com",
            "Did not receive expected email",
        )


class CompanyUploadDocumentsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def setUp(self):
        pass

    def test_upload_document_to_company(self):
        """
        Uploads a single document to a company
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        company = create_company_obj(random_info=False)
        company.allowed_admins.add(c.user)

        data = dict(
            name="Test",
            document=SimpleUploadedFile(
                name="Test File.pdf",
                content=b"This is a test PDF.",
                content_type="application/pdf",
            ),
        )

        res = c.client.post(
            path=f"/companies/{company.id}/upload-document",
            data=data,
        )

        self.assertEqual(res.status_code, 201, f"Expected 201. Got {res.status_code}")
        self.assertIn("documents", res.data, "Did not find expected key")
        self.assertEqual(res.data["documents"][0]["name"], "Test", "Name did not match")
        self.assertTrue(
            res.data["documents"][0]["document"].startswith(
                "/media/documents/Test_File"
            ),
            "Name did not match",
        )
        self.assertEqual(
            res.data["documents"][0]["uploaded_by"]["get_name"],
            c.username,
            "Username does not match",
        )

        for f in listdir(os_join(BASE_DIR, "public/media/documents")):
            if f.startswith("Test_File"):
                os_remove(os_join(BASE_DIR, f"public/media/documents/{f}"))

    def test_upload_document_fails_with_user_not_admin_in_company(self):
        """
        Document uploads fails when user does not have admin permissions
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        company = create_company_obj(random_info=False)

        data = dict(
            name="Test",
            document=SimpleUploadedFile(
                name="Test File.pdf",
                content=b"This is a test PDF.",
                content_type="application/pdf",
            ),
        )

        res = c.client.post(
            path=f"/companies/{company.id}/upload-document",
            data=data,
        )

        self.assertEqual(res.status_code, 400, f"Expected 400. Got {res.status_code}")
        self.assertIn("invite-error", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["invite-error"],
            "invalid invite permissions for requested company",
            "Custom message did not match",
        )
        self.assertIn("detail", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["detail"],
            "Can not invite user to company with ID 1",
            "Custom message did not match",
        )

    def test_upload_document_fails_when_user_has_viewer_status_in_company(self):
        """
        Document uploads fails when user only has viewer status
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        company = create_company_obj(random_info=False)
        company.allowed_viewers.add(c.user)

        data = dict(
            name="Test",
            document=SimpleUploadedFile(
                name="Test File.pdf",
                content=b"This is a test PDF.",
                content_type="application/pdf",
            ),
        )

        res = c.client.post(
            path=f"/companies/{company.id}/upload-document",
            data=data,
        )

        self.assertEqual(res.status_code, 400, f"Expected 400. Got {res.status_code}")
        self.assertIn("invite-error", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["invite-error"],
            "invalid invite permissions for requested company",
            "Custom message did not match",
        )
        self.assertIn("detail", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["detail"],
            "Can not invite user to company with ID 1",
            "Custom message did not match",
        )

    def test_upload_document_fails_when_unauthenticated_user_tries_to_upload_document(
        self,
    ):
        """
        Unregistered user can not upload document
        """
        c = CreateCustomerViews()

        company = create_company_obj(random_info=False)

        data = dict(
            name="Test",
            document=SimpleUploadedFile(
                name="Test File.pdf",
                content=b"This is a test PDF.",
                content_type="application/pdf",
            ),
        )

        res = c.client.post(
            path=f"/companies/{company.id}/upload-document",
            data=data,
        )

        self.assertEqual(res.status_code, 401, f"Expected 401. Got {res.status_code}")
        self.assertTrue("detail" in res.data, "'detail' not in response dict")
        self.assertEqual(
            str(res.data["detail"]),
            "Authentication credentials were not provided.",
            "Did not get the expected error message",
        )
        self.assertEqual(
            res.data["detail"].code,
            "not_authenticated",
            "Did not receive the correct error code",
        )
