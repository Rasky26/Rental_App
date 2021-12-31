from django.test import TestCase
from general_ledger.models import GeneralLedgerCodes
from notes.tests.generic_functions import random_string, random_sentence
from notes.tests.test_models import create_note
import random
import string


def get_general_ledger(name=None, code=None, description=None):
    """
    Creates a general ledger account.
    """
    if name is None:
        name = random_string(text=string.ascii_letters).title()
    if code is None:
        code = random_string(length=11)
    if description is None:
        description = random_sentence(allow_numbers=False)

    obj = GeneralLedgerCodes.objects.create(
        name=name, code=code, description=description
    )

    return {
        "name": name,
        "code": code,
        "description": description,
    }


def create_general_ledger_obj(name=None, code=None, description=None):
    """
    Creates / returns a general ledger object.
    """
    if name is None:
        name = random_string(text=string.ascii_letters).title()
    if code is None:
        code = random_string(length=11)
    if description is None:
        description = random_sentence(allow_numbers=False)

    return GeneralLedgerCodes.objects.create(
        name=name, code=code, description=description
    )


class GeneralLedgerCodesModelsTestCase(TestCase):
    """
    Tests the general ledger model for errors.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def setUp(self):
        pass

    def test_general_ledger_string_all_fields(self):
        """
        Checks that the return object provides the expected string and all values match
        """
        gl_info = create_general_ledger_obj(
            name="Test GL", code="1234567890", description="Test GL Description"
        )
        self.assertEqual(
            str(gl_info),
            "Test GL | 1234567890",
            "General ledger return string mis-match",
        )
        self.assertEqual(gl_info.name, "Test GL", "GL name did not match")
        self.assertEqual(gl_info.code, "1234567890", "Did not get the expected GL code")
        self.assertEqual(
            gl_info.description,
            "Test GL Description",
            "Did not get the expected GL description",
        )
        self.assertFalse(gl_info.notes.all(), "General ledger notes not empty")

    def test_general_ledger_string_no_code(self):
        """
        Checks the return string if no gl code is provided
        """
        gl_info = create_general_ledger_obj(name="Test GL", code="")
        self.assertEqual(str(gl_info), "Test GL", "Return string does not match")

    def test_attached_notes_to_general_ledger(self):
        """
        Check that the note text matches
        """
        note = create_note(text="Test note")
        gl_info = create_general_ledger_obj()
        gl_info.notes.add(note)
        self.assertEqual(
            gl_info.notes.all().first().note,
            "Test note",
            "General ledger note does not match",
        )
