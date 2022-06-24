from accounts.tests.test_models import CreateUser
from buildings.models import Buildings
from companies.tests.test_models import create_company_obj
from contacts.tests.test_models import create_address_obj
from datetime import datetime
from django.test import TestCase
from general_ledger.tests.test_models import create_general_ledger_obj
from notes.tests.generic_functions import random_length_string
from notes.tests.test_models import create_note
from random import randint


def create_building_obj(
    random_info=True,
    num_allowed_admins=0,
    num_allowed_viewers=0,
    num_notes=0,
):
    """
    Creates a building object for easy testing
    """

    if random_info:
        building = Buildings.objects.create(
            company=create_company_obj(random_info),
            name=random_length_string(low=4, high=16, allow_digits=False).title(),
            address=create_address_obj(random_address=True),
            gl_code=create_general_ledger_obj(),
            build_year=datetime(randint(1900, 2020), randint(1, 12), 1).date(),
        )
        for _ in range(num_allowed_admins):
            u = CreateUser()
            u.create_user()
            building.allowed_admins.add(u.user)
        for _ in range(num_allowed_viewers):
            u = CreateUser()
            u.create_user()
            building.allowed_viewers.add(u.user)
        u = CreateUser()
        u.create_user()
        for _ in range(num_notes):
            building.notes.add(create_note(user=u.user))

    else:
        building = Buildings.objects.create(
            company=create_company_obj(random_info=False),
            name="Test",
            address=create_address_obj(random_address=False),
            gl_code=create_general_ledger_obj(name="Test"),
            build_year=datetime(1970, 1, 1).date(),
        )

    return building


class BuildingsModelsTestCase(TestCase):
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

    def test_building_creation(self):
        """
        Tests that a building can be saved successfully to a model
        """
        building = create_building_obj(
            random_info=True, num_allowed_admins=3, num_allowed_viewers=4, num_notes=5
        )

        self.assertEqual(
            str(building),
            f"{building.company.company_name} | {building.name}",
            "Did not received expected string",
        )
        self.assertFalse(building.accounts_payable_extension, "Did not get False")
        self.assertFalse(building.accounts_receivable_extension, "Did not get False")
        self.assertFalse(building.maintenance_extension, "Did not get False")
        self.assertEqual(
            len(building.allowed_admins.all()),
            3,
            "Did not get the expected number of admin users",
        )
        self.assertEqual(
            len(building.allowed_viewers.all()),
            4,
            "Did not get the expected number of viewer users",
        )
        self.assertEqual(
            len(building.notes.all()), 5, "Did not get the expected number of notes"
        )
