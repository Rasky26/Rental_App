from accounts.tests.test_views import CreateCustomerViews
from buildings.models import Buildings
from contacts.tests.test_views import get_address_data
from datetime import datetime
from django.test import TestCase
from notes.tests.generic_functions import (
    random_bell_curve_int,
    random_sentence,
    random_string,
)
from random import randint
import json
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


class BuildingsViewsTestCase(TestCase):
    """
    Tests the buildings model for errors
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
        Creates a building without an existing company.

        Automatically creates a company, the core GL accounts, and the building linked to a generic building
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
