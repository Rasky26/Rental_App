from contacts.models import Addresses, Contacts
from django.test import TestCase
from notes.tests.generic_functions import (
    random_bell_curve_int,
    random_sentence,
    random_string,
)
import string


def default_address():
    """
    Default address to use
    """
    return Addresses.objects.create(
        address1="111 1st. St. S",
        address2="Apt. 1",
        city="City",
        state="MN",
        zipcode="55555-5555",
    )


def create_address_obj(random_address=False):
    """
    Creates a generic address object for easy testing.
    """
    if not random_address:
        return default_address()
    return Addresses.objects.create(
        address1=random_sentence(total_len=random_bell_curve_int(low=8, high=24)),
        address2=random_string(length=8),
        city=random_string(
            length=random_bell_curve_int(low=4, high=16), text=string.ascii_letters
        ).title(),
        state="MN",
        zipcode=random_string(length=5, text=string.digits),
    )


def default_contact():
    """
    Default contact to use.
    """
    return Contacts.objects.create(
        name_first="John",
        name_last="Doe",
        phone_1="5551234567",
        email="John.Doe@email.com",
    )


def create_contact_obj(random_contact=False):
    """
    Creates a generic contact object for easy testing.
    """
    if not random_contact:
        return default_contact()
    return Contacts.objects.create(
        name_first=random_string(length=5, text=string.ascii_letters.title()),
        name_last=random_string(length=8, text=string.ascii_letters.title()),
        phone_1=random_string(length=10, text=string.digits),
        email=random_string(length=7, text=string.ascii_letters) + "@email.com",
    )


class AddressesModelsTestCase(TestCase):
    """
    Tests the address model for errors
    """

    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def setUp(self):
        Addresses.objects.create(
            address1="111 1st. St. S",
            address2="Apt. 1",
            city="City",
            state="MN",
            zipcode="55555",
        )
        Addresses.objects.create(
            address1="222 1st. St. S",
            city="City",
            state="MN",
            zipcode="55555",
        )
        Addresses.objects.create(
            address1="333 1st. St. S",
            address2="Apt. 1",
            state="MN",
            zipcode="55555",
        )
        Addresses.objects.create(
            address1="444 1st. St. S",
            address2="Apt. 1",
            city="City",
            zipcode="55555",
        )
        Addresses.objects.create(
            address1="555 1st. St. S",
            address2="Apt. 1",
            city="City",
            state="MN",
        )
        Addresses.objects.create(
            address1="666 1st. St. S",
            address2="Apt. 1",
            city="City",
            state="MN",
            zipcode="55555-5555",
        )
        Addresses.objects.create(
            address2="Apt. 2",
            city="Town",
            state="WI",
            zipcode="44444",
        )

    def test_address_full(self):
        """
        Tests the string return for the full address
        """
        address = Addresses.objects.get(address1="111 1st. St. S")
        self.assertEqual(
            str(address),
            "111 1st. St. S, Apt. 1, City, MN 55555",
            "Address string not matching",
        )

    def test_address_no_address_2(self):
        """
        Tests the string return for the full address
        """
        address = Addresses.objects.get(address1="222 1st. St. S")
        self.assertEqual(
            str(address),
            "222 1st. St. S, City, MN 55555",
            "Address string not matching",
        )

    def test_address_no_city(self):
        """
        Tests the string return for the full address
        """
        address = Addresses.objects.get(address1="333 1st. St. S")
        self.assertEqual(
            str(address),
            "333 1st. St. S, Apt. 1, MN 55555",
            "Address string not matching",
        )

    def test_address_no_state(self):
        """
        Tests the string return for the full address
        """
        address = Addresses.objects.get(address1="444 1st. St. S")
        self.assertEqual(
            str(address),
            "444 1st. St. S, Apt. 1, City 55555",
            "Address string not matching",
        )

    def test_address_no_zipcode(self):
        """
        Tests the string return for the full address
        """
        address = Addresses.objects.get(address1="555 1st. St. S")
        self.assertEqual(
            str(address),
            "555 1st. St. S, Apt. 1, City, MN",
            "Address string not matching",
        )

    def test_address_long_zipcode(self):
        """
        Tests the string return for the full address
        """
        address = Addresses.objects.get(address1="666 1st. St. S")
        self.assertEqual(
            str(address),
            "666 1st. St. S, Apt. 1, City, MN 55555-5555",
            "Address string not matching",
        )

    def test_no_address_1(self):
        """
        Tests the string return for the full address
        """
        address = Addresses.objects.get(address2="Apt. 2", city="Town")
        self.assertEqual(
            str(address),
            "Apt. 2, Town, WI 44444",
            "Address string not matching",
        )
