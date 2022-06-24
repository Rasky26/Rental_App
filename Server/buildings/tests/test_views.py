from accounts.tests.test_views import CreateCustomerViews
from buildings.models import Buildings
from buildings.tests.test_models import create_building_obj
from change_log.models import ChangeLog
from companies.tests.test_models import create_company_obj
from contacts.tests.test_views import get_address_data
from datetime import datetime
from django.test import TestCase
from notes.tests.generic_functions import (
    random_bell_curve_int,
    random_sentence,
    random_string,
)
from random import randint
from unittest import mock
import json
import pytz
import string
from pprint import pprint


def building_no_company_data(
    random_info=True, name=None, random_address=True, build_year=None, num_notes=2
):
    """
    Return data JSON to quickly create a building
    """
    if random_info:
        building = dict(
            name=random_string(text=string.ascii_letters).title(),
            address=get_address_data(random_address=True),
            build_year=datetime(randint(1900, 2020), randint(1, 12), 1).date(),
            notes=[
                dict(
                    note=random_sentence(
                        total_len=random_bell_curve_int(low=1, high=128)
                    )
                )
                for _ in range(num_notes)
            ],
        )

    else:
        building = dict(
            name="Test",
            address=get_address_data(random_address=False),
            build_year=datetime(1970, 1, 1).date(),
            notes=[dict(note="Note 1"), dict(note="Note 2")],
        )

    return building


class BuildingsWithNoCompanyViewsTestCase(TestCase):
    """
    Tests the creation of a building with no existing company to link it to
    """

    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def setUp(self):
        pass

    def test_create_building_no_company(self):
        """
        Creates a building without an existing company.

        Automatically creates a company, the core GL accounts, and the building linked to a generic building
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        res = c.client.post(
            path="/buildings/no-company/new-building",
            data=building_no_company_data(random_info=False),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 201, f"Expected 201. Got {res.status_code}")
        self.assertEqual(res.data["name"], "Test", "Did not get correct name")
        self.assertEqual(
            res.data["address"]["address_1"], "111 1st St. S", "Wrong address 1"
        )
        self.assertEqual(res.data["build_year"], "1970-01-01", "Incorrect start year")
        self.assertFalse(res.data["documents"], "Documents existed with object")
        self.assertFalse(res.data["images"], "Images existed with object")
        self.assertEqual(
            len(res.data["notes"]), 2, f"Expected 2 notes, got {len(res.data['notes'])}"
        )

        building_obj = Buildings.objects.get(id=1)

        self.assertEqual(
            building_obj.company.business_name,
            "Rental Business",
            "Did not get expected default name",
        )
        self.assertEqual(
            building_obj.company.accounts_receivable_gl.name,
            "Accounts Receivable",
            "Wrong default general ledger name",
        )
        self.assertEqual(
            building_obj.company.accounts_payable_gl.name,
            "Accounts Payable",
            "Wrong default general ledger name",
        )
        self.assertEqual(
            building_obj.company.gl_code.name,
            "Rental Business",
            "Wrong default general ledger name",
        )
        self.assertIn(
            c.user,
            building_obj.company.allowed_admins.all(),
            "User not automatically set to admin in company",
        )

    def test_unauthenticated_user_can_not_create_building_no_company(self):
        """
        Users without token get expected error message
        """
        c = CreateCustomerViews()

        res = c.client.post(
            path="/buildings/no-company/new-building",
            data=building_no_company_data(random_info=False),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 401, f"Expected 401. Got {res.status_code}")
        self.assertIn("detail", res.data, "Error field not found")
        self.assertEqual(
            res.data["detail"],
            "Authentication credentials were not provided.",
            "Wrong error string",
        )
        self.assertEqual(
            res.data["detail"].code, "not_authenticated", "Wrong error code"
        )

    def test_create_building_no_company_minimum_information(self):
        """
        Creates a building using only the core information. Creates containing company too.
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        res = c.client.post(
            path="/buildings/no-company/new-building",
            data=dict(name="Test"),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 201, f"Expected 201. Got {res.status_code}")
        self.assertEqual(res.data["name"], "Test", "Did not get expected name")
        self.assertIsNone(res.data["address"], "Address was not None")
        self.assertIsNone(res.data["build_year"], "Build year was not None")
        self.assertFalse(res.data["documents"], "Documents array was not empty")
        self.assertFalse(res.data["images"], "Images array was not empty")
        self.assertFalse(res.data["notes"], "Notes array was not empty")

        building_obj = Buildings.objects.get(id=1)

        self.assertEqual(
            building_obj.company.business_name,
            "Rental Business",
            "Did not get expected default name",
        )
        self.assertEqual(
            building_obj.company.accounts_receivable_gl.name,
            "Accounts Receivable",
            "Wrong default general ledger name",
        )
        self.assertEqual(
            building_obj.company.accounts_payable_gl.name,
            "Accounts Payable",
            "Wrong default general ledger name",
        )
        self.assertEqual(
            building_obj.company.gl_code.name,
            "Rental Business",
            "Wrong default general ledger name",
        )
        self.assertIn(
            c.user,
            building_obj.company.allowed_admins.all(),
            "User not automatically set to admin in company",
        )

    def test_create_building_no_company_no_information_provided(self):
        """
        Fails if no name is passed.
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        res = c.client.post(
            path="/buildings/no-company/new-building",
            data=None,
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 400, f"Expected 400. Got {res.status_code}")
        self.assertIn("building-errors", res.data, "Did not find expected key")
        self.assertIn("name", res.data["building-errors"], "Did not find expected key")
        self.assertEqual(
            str(res.data["building-errors"]["name"][0]),
            "This field is required.",
            "Did not get expected error message",
        )
        self.assertEqual(
            res.data["building-errors"]["name"][0].code,
            "required",
            "Did not find expected key",
        )


class BuildingsWithExistingCompanyViewsTestCase(TestCase):
    """
    Creation of company with a company that it can be assigned to
    """

    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def setUp(self):
        pass

    def test_create_building_no_company(self):
        """
        Creates a building with an existing company.
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        company = create_company_obj(random_info=False)
        company.allowed_admins.add(c.user)

        res = c.client.post(
            path=f"/buildings/{company.id}/new-building",
            data=building_no_company_data(random_info=False),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 201, f"Expected 201. Got {res.status_code}")
        self.assertEqual(res.data["name"], "Test", "Did not get correct name")
        self.assertEqual(
            res.data["address"]["address_1"], "111 1st St. S", "Wrong address 1"
        )
        self.assertEqual(res.data["build_year"], "1970-01-01", "Incorrect start year")
        self.assertFalse(res.data["documents"], "Documents existed with object")
        self.assertFalse(res.data["images"], "Images existed with object")
        self.assertEqual(
            len(res.data["notes"]), 2, f"Expected 2 notes, got {len(res.data['notes'])}"
        )

        building = Buildings.objects.get(id=res.data["id"])

        self.assertEqual(
            str(building.company),
            "Test | Test LLC",
            "Did not get he expected company name",
        )
        self.assertEqual(
            str(building.gl_code), "Test", "Did not get the expected GL Code name"
        )

    def test_building_creation_fails_if_not_admin_in_company(self):
        """
        If the user does not have admin permissions in the company, creation fails
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        company = create_company_obj(random_info=False)

        res = c.client.post(
            path=f"/buildings/{company.id}/new-building",
            data=building_no_company_data(random_info=False),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 400, f"Expected 400. Got {res.status_code}")
        self.assertIn("invite-error", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["invite-error"],
            "Invalid invite permissions for requested company",
            "Error message mis-match",
        )
        self.assertIn("detail", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["detail"],
            "Can not invite user to company with ID 1",
            "Error message mis-match",
        )

    def test_building_creation_fails_if_invalid_company_id_provided(self):
        """
        Building creation fails if an invalid building PK is provided
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        res = c.client.post(
            path=f"/buildings/1234/new-building",
            data=building_no_company_data(random_info=False),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 400, f"Expected 400. Got {res.status_code}")
        self.assertIn("invite-error", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["invite-error"],
            "Invalid invite permissions for requested company",
            "Error message mis-match",
        )
        self.assertIn("detail", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["detail"],
            "Can not invite user to company with ID 1234",
            "Error message mis-match",
        )


class BuildingsUpdateViewsTestCase(TestCase):
    """
    Creation of company with a company that it can be assigned to
    """

    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def setUp(self):
        pass

    def test_retrieve_building_info(self):
        """
        Test that a user with correct permissions can view a building.
        """
        c = CreateCustomerViews(
            username="Test", email="test@email.com", password="123456789"
        )
        c.create_user()
        c.login()

        building = create_building_obj(random_info=False)
        building.company.allowed_admins.add(c.user)

        res = c.client.get(
            path=f"/buildings/{building.id}/update",
        )

        self.assertEqual(res.status_code, 200, f"Expected 200. Got {res.status_code}")
        self.assertEqual(res.data["name"], "Test", "Did not get expected name")
        self.assertEqual(
            res.data["build_year"], "1970-01-01", "Did not get expected year"
        )

    def test_update_building_info(self):
        """
        Update a building's information, save original information to the change log.
        """
        c = CreateCustomerViews(
            username="Test", email="test@email.com", password="123456789"
        )
        c.create_user()
        c.login()

        building = create_building_obj(random_info=False)
        building.company.allowed_admins.add(c.user)

        # Set outdated timestamp
        mocked = datetime(2021, 12, 1, 0, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):

            res = c.client.patch(
                path=f"/buildings/{building.id}/update",
                data=dict(name="Testing", build_year=datetime(1950, 1, 1).date()),
                content_type="application/json",
            )

        self.assertEqual(res.status_code, 200, f"Expected 200. Got {res.status_code}")
        self.assertNotEqual(
            res.data["name"], "Test", "Updated name matched previous value"
        )
        self.assertEqual(
            res.data["name"], "Testing", "Updated name did not match expected value"
        )
        self.assertEqual(res.data["id"], building.id, "Reference Building PK mis-match")

        # Check that previous values were properly saved to the change log
        change_log = ChangeLog.objects.all()
        change_1 = change_log.get(id=1)
        change_2 = change_log.get(id=2)

        self.assertEqual(
            str(change_1),
            "12:00 AM - Dec. 01, 2021 | table: 'Buildings: PK 1' - 'name: str(Test)' | Previous author: Test",
            "Change log text not matching",
        )
        self.assertEqual(
            str(change_2),
            "12:00 AM - Dec. 01, 2021 | table: 'Buildings: PK 1' - 'build_year: date(1970-01-01)' | Previous author: Test",
            "Change log text not matching",
        )

    def test_update_building_info_fails_when_user_does_not_have_admin_permissions(self):
        """
        Update fails when user not in the allowed_admins
        """
        c = CreateCustomerViews(
            username="Test", email="test@email.com", password="123456789"
        )
        c.create_user()
        c.login()

        building = create_building_obj(random_info=False)

        res = c.client.patch(
            path=f"/buildings/{building.id}/update",
            data=dict(name="Testing", build_year=datetime(1950, 1, 1).date()),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 400, f"Expected 400. Got {res.status_code}")
        self.assertIn("invite-error", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["invite-error"],
            "Invalid invite permissions for requested building",
            "Error message mis-match",
        )
        self.assertIn("detail", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["detail"],
            "Can not invite user to building with ID 1",
            "Error message mis-match",
        )

    def test_update_building_info_allowed_when_company_viewer_but_building_admin(self):
        """
        Allows an update when the user has building admin permissions, even if the company is only set to viewer
        """
        c = CreateCustomerViews(
            username="Test", email="test@email.com", password="123456789"
        )
        c.create_user()
        c.login()

        building = create_building_obj(random_info=False)
        building.company.allowed_viewers.add(c.user)
        building.allowed_admins.add(c.user)

        # Set outdated timestamp
        mocked = datetime(2021, 12, 1, 0, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):

            res = c.client.patch(
                path=f"/buildings/{building.id}/update",
                data=dict(name="Testing", build_year=datetime(1950, 1, 1).date()),
                content_type="application/json",
            )

        self.assertEqual(res.status_code, 200, f"Expected 200. Got {res.status_code}")
        self.assertNotEqual(
            res.data["name"], "Test", "Updated name matched previous value"
        )
        self.assertEqual(
            res.data["name"], "Testing", "Updated name did not match expected value"
        )
        self.assertEqual(res.data["id"], building.id, "Reference Building PK mis-match")

        # Check that previous values were properly saved to the change log
        change_log = ChangeLog.objects.all()
        change_1 = change_log.get(id=1)
        change_2 = change_log.get(id=2)

        self.assertEqual(
            str(change_1),
            "12:00 AM - Dec. 01, 2021 | table: 'Buildings: PK 1' - 'name: str(Test)' | Previous author: Test",
            "Change log text not matching",
        )
        self.assertEqual(
            str(change_2),
            "12:00 AM - Dec. 01, 2021 | table: 'Buildings: PK 1' - 'build_year: date(1970-01-01)' | Previous author: Test",
            "Change log text not matching",
        )

    def test_update_building_info_fails_when_user_only_has_building_viewer_permissions(
        self,
    ):
        """
        Update fails when the user only has building viewer permissions, despite having company admin privileges
        """
        c = CreateCustomerViews(
            username="Test", email="test@email.com", password="123456789"
        )
        c.create_user()
        c.login()

        building = create_building_obj(random_info=False)
        building.company.allowed_admins.add(c.user)
        building.allowed_viewers.add(c.user)

        res = c.client.patch(
            path=f"/buildings/{building.id}/update",
            data=dict(name="Testing", build_year=datetime(1950, 1, 1).date()),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 400, f"Expected 400. Got {res.status_code}")
        self.assertIn("invite-error", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["invite-error"],
            "Invalid invite permissions for requested building",
            "Error message mis-match",
        )
        self.assertIn("detail", res.data, "Did not find expected key")
        self.assertEqual(
            res.data["detail"],
            "Can not invite user to building with ID 1",
            "Error message mis-match",
        )


class BuildingsRetrieveViewsTestCase(TestCase):
    """
    Creation of company with a company that it can be assigned to
    """

    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def setUp(self):
        pass
