from accounts.tests.test_views import CreateCustomerViews
from companies.tests.test_models import create_company_obj
from contacts.tests.test_views import get_address_data, get_contact_data
from django.test import Client, TestCase
from notes.tests.generic_functions import (
    random_bell_curve_int,
    random_string,
    random_sentence,
)
import string
from pprint import pprint


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
        # print(
        #     "setUpTestData: Run once to set up non-modified data for all class methods."
        # )
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
            f"{res.data['business_address']['address1']} {res.data['business_address']['address2']} {res.data['business_address']['city']} {res.data['business_address']['state']} {res.data['business_address']['zipcode']}",
            "111 1st St. S Apt. 1 City MN 55555-5555",
            "Did not get the correct business address",
        )
        self.assertEqual(
            f"{res.data['mailing_address']['address1']} {res.data['mailing_address']['address2']} {res.data['mailing_address']['city']} {res.data['mailing_address']['state']} {res.data['mailing_address']['zipcode']}",
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
        self.assertIn(
            c.user,
            res.data["allowed_admins"],
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
            address1="", address2="", city="", state="", zipcode=""
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
            address1="111 1st St. S", address2="", city="", state="", zipcode=""
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
            f"{m['address1']}{m['address2']}{m['city']}{m['state']}{m['zipcode']}",
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
        # print(
        #     "setUpTestData: Run once to set up non-modified data for all class methods."
        # )
        return super().setUpTestData()

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def setUp(self):
        pass

    def test_set_admin_invite_to_company(self):
        """
        Creates admin invite to company
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        company = create_company_obj()

        res = c.client.post(
            path=f"/companies/invite/{company.id}",
            data=None,
            content_type="application/json",
        )

        print(res)
