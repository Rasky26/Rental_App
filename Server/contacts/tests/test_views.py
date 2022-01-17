from django.test import TestCase
from notes.tests.generic_functions import (
    random_bell_curve_int,
    random_length_string,
    random_sentence,
    random_string,
)
from random import choice
import string


def get_address_data(random_address=True):
    """
    Returns an address dictionary for quick testing
    """
    if random_address:
        return dict(
            address_1=random_sentence(total_len=random_bell_curve_int(low=8, high=20)),
            address_2=random_length_string(low=6, high=12),
            city=random_length_string(low=4, high=20, allow_digits=False).title(),
            state="MN",
            zipcode=random_string(length=5, text=string.digits),
        )

    return dict(
        address_1="111 1st St. S",
        address_2="Apt. 1",
        city="City",
        state="MN",
        zipcode="55555-5555",
    )


def get_contact_data(random_contact=True):
    """
    Returns a contact dictionary for quick testing
    """
    if random_contact:
        return dict(
            name_prefix=random_length_string(high=4, allow_digits=False).title(),
            name_first=random_length_string(low=4, high=12, allow_digits=False).title(),
            name_middle=random_length_string(
                low=2, high=12, allow_digits=False
            ).title(),
            name_last=random_length_string(low=2, high=14, allow_digits=False).title(),
            name_suffix=random_length_string(high=3, allow_digits=False).title(),
            phone_1=random_string(length=10, text=string.digits),
            phone_2=random_string(length=10, text=string.digits),
            email=f"{random_length_string(low=4,high=12,allow_digits=False)}@email.com",
        )

    return dict(
        name_prefix="Mr.",
        name_first="John",
        name_middle="E",
        name_last="Doe",
        name_suffix="Esq.",
        phone_1="1234567890",
        phone_2="9876543210",
        email="john@email.com",
    )


class AddressesViewsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def setUp(self):
        pass
