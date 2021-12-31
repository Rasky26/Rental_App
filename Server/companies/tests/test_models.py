from accounts.tests.test_models import create_user_obj, CreateUser
from companies.models import Companies, CompanyInviteList
from contacts.tests.test_models import create_address_obj, create_contact_obj
from django.test import TestCase
from general_ledger.tests.test_models import create_general_ledger_obj
from notes.tests.generic_functions import (
    random_bell_curve_int,
    random_length_string,
    random_string,
)
from notes.tests.test_models import create_note
import string


def create_company_obj(
    random_info=True,
    num_contacts=0,
    num_allowed_admins=0,
    num_allowed_viewers=0,
    num_notes=0,
):
    """
    Creates a generic company object for easy testing.
    """
    if random_info:
        name = random_length_string(low=4, high=16, allow_digits=False).title()
        company = Companies.objects.create(
            business_name=name,
            legal_name=f"{name} LLC",
            business_address=create_address_obj(random_address=True),
            mailing_address=create_address_obj(random_address=True),
            gl_code=create_general_ledger_obj(),
            accounts_payable_gl=create_general_ledger_obj(),
            accounts_receivable_gl=create_general_ledger_obj(),
        )
        for _ in range(num_contacts):
            company.contacts.add(create_contact_obj(random_contact=True))
        for _ in range(num_allowed_admins):
            u = CreateUser()
            u.create_user()
            company.allowed_admins.add(u.user)
        for _ in range(num_allowed_viewers):
            u = CreateUser()
            u.create_user()
            company.allowed_viewers.add(u.user)
        u = CreateUser()
        u.create_user()
        for _ in range(num_notes):
            company.notes.add(create_note(user=u.user))

    else:
        company = Companies.objects.create(
            business_name="Test",
            legal_name="Test LLC",
            business_address=create_address_obj(random_address=False),
            mailing_address=create_address_obj(random_address=False),
            gl_code=create_general_ledger_obj(name="Test"),
            accounts_payable_gl=create_general_ledger_obj(name="AP GL"),
            accounts_receivable_gl=create_general_ledger_obj(name="AR GL"),
        )

    return company


def create_company_invite(company_obj=None, email=None, admin_in=False, viewer_in=True):
    """
    Create a generic company invite for a user.
    """
    if not company_obj:
        company_obj = create_company_obj()
    if not email:
        email = (
            f"{random_string(length=random_bell_curve_int(low=4,high=20))}@email.com"
        )
    if admin_in:
        admin_in = company_obj
        viewer_in = None
    if viewer_in:
        admin_in = None
        viewer_in = company_obj
    return CompanyInviteList.objects.create(
        email=email, admin_in=admin_in, viewer_in=viewer_in
    )


class CompaniesModelsTestCase(TestCase):
    """
    Tests the companies model for errors
    """

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
        Create a company and check return string
        """
        company = create_company_obj(random_info=False)
        self.assertEqual(
            str(company),
            f"{company.business_name} | {company.legal_name}",
            "Did not received expected string",
        )
        self.assertFalse(company.accounts_payable_extension, "Did not get False")
        self.assertFalse(company.accounts_receivable_extension, "Did not get False")
        self.assertFalse(company.maintenance_extension, "Did not get False")

    def test_company_return_string_with_no_legal_name(self):
        """
        Checks the return string if there is not legal name
        """
        company = create_company_obj(random_info=False)
        company.legal_name = ""
        company.save()
        self.assertEqual(
            str(company),
            f"{company.business_name}",
            "Did not received expected string",
        )

    def test_company_with_expected_number_of_contacts(self):
        """
        Checks that the assigned number of contacts are added in the ManyToMany field
        """
        company = create_company_obj(num_contacts=10)
        self.assertEqual(
            len(company.contacts.all()),
            10,
            f"Expected 10 contacts. Got {len(company.contacts.all())} instead",
        )

    def test_company_with_expected_number_of_allowed_admins(self):
        """
        Checks that the assigned number of allowed_user are added in the ManyToMany field
        """
        company = create_company_obj(num_allowed_admins=10)
        self.assertEqual(
            len(company.allowed_admins.all()),
            10,
            f"Expected 10 allowed_admins. Got {len(company.allowed_admins.all())} instead",
        )

    def test_company_with_expected_number_of_allowed_viewers(self):
        """
        Checks that the assigned number of allowed_user are added in the ManyToMany field
        """
        company = create_company_obj(num_allowed_viewers=10)
        self.assertEqual(
            len(company.allowed_viewers.all()),
            10,
            f"Expected 10 allowed_viewers. Got {len(company.allowed_viewers.all())} instead",
        )

    def test_company_with_expected_number_of_notes(self):
        """
        Checks that the assigned number of allowed_user are added in the ManyToMany field
        """
        company = create_company_obj(num_notes=10)
        self.assertEqual(
            len(company.notes.all()),
            10,
            f"Expected 10 notes. Got {len(company.notes.all())} instead",
        )


class CompaniesInviteListModelsTestCase(TestCase):
    """
    Tests the companies model for errors
    """

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

    def test_company_viewer_invite(self):
        """
        Admin invititation for a company
        """
        invite = create_company_invite(email="test@email.com")
        self.assertEqual(str(invite), "test@email.com - Viewer Invitation")

    def test_company_admin_invite(self):
        """
        Admin invititation for a company
        """
        invite = create_company_invite(
            email="test@email.com", admin_in=True, viewer_in=False
        )
        self.assertEqual(str(invite), "test@email.com - Admin Invitation")

    def test_no_duplicate_admin_invites_for_company(self):
        """
        Do not allow duplicate company invites for admin user
        """
        company = create_company_obj()
        email = "test@email.com"

        CompanyInviteList.objects.create(email=email, admin_in=company, viewer_in=None)
        self.assertEqual(
            len(CompanyInviteList.objects.filter(email="test@email.com")),
            1,
            "Expected 1 invite",
        )

        CompanyInviteList.objects.create(email=email, admin_in=company, viewer_in=None)
        self.assertEqual(
            len(CompanyInviteList.objects.filter(email="test@email.com")),
            1,
            "Expected 1 invite",
        )
