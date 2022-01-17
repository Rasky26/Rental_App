from contacts.functions import populate_address_dict
from django.test import TestCase


class PopulateAddressDictTestCase(TestCase):
    """
    Tests the address model for errors
    """

    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def setUp(self) -> None:
        return super().setUp()

    def test_none_value_changed_to_blank_dict(self):
        """
        Make sure a None value returns a blank dict
        """
        res = populate_address_dict(None)
        self.assertFalse(any(res.values()), "Return address dict was not empty")

    def test_blank_address_dict_remains_blank(self):
        """
        Ensures a blank address dictionary is unchanged
        """
        res = populate_address_dict(
            dict(address_1="", address_2="", city="", state="", zipcode="")
        )
        self.assertEqual(
            res,
            dict(address_1="", address_2="", city="", state="", zipcode=""),
            "Did not get matching empty dict",
        )

    def test_dict_with_too_few_fields_returns_expected_dict(self):
        """
        If too few fields are sent, make sure an expected dict of fields returns
        """
        res = populate_address_dict(dict(address_1="", address_2=""))
        self.assertEqual(
            res,
            dict(address_1="", address_2="", city="", state="", zipcode=""),
            "Did not get matching dict",
        )

    def test_extra_fields_remain_in_dictionary(self):
        """
        Checks that extra, unaccounted, fields are returned unchanged
        """
        res = populate_address_dict(
            dict(
                address_1="",
                address_2="",
                city="",
                state="",
                zipcode="",
                extra_info="  123 . ",
            )
        )
        self.assertEqual(
            res,
            dict(
                address_1="",
                address_2="",
                city="",
                state="",
                zipcode="",
                extra_info="  123 . ",
            ),
            "Did not get matching dict",
        )

    def test_normal_dict_is_unchanged(self):
        """
        Data in should match data out
        """
        res = populate_address_dict(
            dict(
                address_1="111 1st St. S",
                address_2="Apt. 1",
                city="City",
                state="MN",
                zipcode="55555-5555",
            )
        )
        self.assertEqual(
            res,
            dict(
                address_1="111 1st St. S",
                address_2="Apt. 1",
                city="City",
                state="MN",
                zipcode="55555-5555",
            ),
            "Did not get matching dict",
        )

    def test_extra_spaces_in_address_data_are_removed(self):
        """
        Removes extra spaces around data for better consistence and storage
        """
        res = populate_address_dict(
            dict(
                address_1="   111  1st  St. S",
                address_2="Apt. 1      ",
                city="   City          ",
                state="     MN           ",
                zipcode=" 55555-5555                   ",
            )
        )
        self.assertEqual(
            res,
            dict(
                address_1="111 1st St. S",
                address_2="Apt. 1",
                city="City",
                state="MN",
                zipcode="55555-5555",
            ),
            "Excess spaces were not removed",
        )

    def test_extra_spaces_in_address_data_are_removed_but_preserved_in_extra_fields(
        self,
    ):
        """
        Does not make modifications to extra fields
        """
        res = populate_address_dict(
            dict(
                address_1="   111  1st  St. S",
                address_2="Apt. 1      ",
                city="   City          ",
                state="     MN           ",
                zipcode=" 55555-5555                   ",
                extra_info="   not  tracked   ",
            )
        )
        self.assertEqual(
            res,
            dict(
                address_1="111 1st St. S",
                address_2="Apt. 1",
                city="City",
                state="MN",
                zipcode="55555-5555",
                extra_info="   not  tracked   ",
            ),
            "Excess spaces were removed from the untracked value",
        )
