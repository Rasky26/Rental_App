from django.test import TestCase
from accounts.tests.test_models import CreateUser
from notes.models import Notes
from notes.tests.generic_functions import random_bell_curve_int, random_sentence
import random
import string


def create_note(text=None, user=None):
    """
    Creates a note of random strings to test against.
    """
    # If no values were passed
    if (not text) and (not user):
        c = CreateUser()
        c.create_user()
        return Notes.objects.create(
            note=random_sentence(
                total_len=random_bell_curve_int(low=4, high=128), allow_numbers=True
            ),
            user=c.user,
        )

    # If no note text was passed
    if not text:
        return Notes.objects.create(
            note=random_sentence(
                total_len=random_bell_curve_int(low=4, high=128), allow_numbers=True
            ),
            user=user,
        )

    # If not user object was passed
    if not user:
        c = CreateUser()
        c.create_user()
        return Notes.objects.create(note=text, user=c.user)

    # If all fields were passed
    return Notes.objects.create(note=text, user=user)


class NoteModelsTestCase(TestCase):
    """
    Test the notes model to check for errors.
    """

    @classmethod
    def setUpTestData(self) -> None:
        return super().setUpTestData()

    @classmethod
    def tearDownClass(self) -> None:
        return super().tearDownClass()

    def setUp(self):
        pass

    def test_note_creation(self):
        """
        Verifies the information of a newly created note
        """
        c = CreateUser()
        c.create_user()
        note = create_note(text="Testing", user=c.user)
        self.assertEqual(note.user_id, c.user.id, "User ID mis-match on Note creation")
        self.assertEqual(note.note, "Testing", "Note text mis-match on Note creation")
        self.assertTrue(note.created_at, "Created at time was not assigned")
        self.assertTrue(note.updated_at, "Updated at time was no assigned")

    def test_note_return_string_short(self):
        """
        Tests the model __str__ for a short note ( <31 chars )
        """
        text = random_sentence(total_len=8)
        note = create_note(text=text)
        self.assertEqual(
            str(note),
            note.created_at.strftime("%#I:%M %p - %b. %d, %Y") + " - " + text,
            "Note text did not match",
        )

    def test_note_return_string_long(self):
        """
        Tests the model __str__ for a long note ( >31 chars )
        """
        text = random_sentence(total_len=800000)
        note = create_note(text=text)
        self.assertEqual(
            str(note),
            f"{note.created_at.strftime('%#I:%M %p - %b. %d, %Y')} - {text[:31]}...",
            "Note text did not match",
        )

    def test_note_return_string_31_chars(self):
        """
        Tests the model __str__ for a short note ( <31 chars )
        """
        text = random_sentence(total_len=31)
        note = create_note(text=text)
        self.assertEqual(
            str(note),
            f"{note.created_at.strftime('%#I:%M %p - %b. %d, %Y')} - {text}",
            "Note text did not match",
        )

    def test_note_return_string_32_chars(self):
        """
        Tests the model __str__ for a short note ( <31 chars )
        """
        text = random_sentence(total_len=32)
        note = create_note(text=text)
        self.assertEqual(
            str(note),
            f"{note.created_at.strftime('%#I:%M %p - %b. %d, %Y')} - {text[:31]}...",
            "Note text did not match",
        )

    def test_note_deletion_leaves_other_note(self):
        """
        Tests that when the previous note is deleted that the current note is removed too.
        """
        note_1 = create_note()
        create_note()
        note_1.delete()
        self.assertEqual(
            Notes.objects.all().count(),
            1,
            f"Expected 1 note, found {Notes.objects.all().count()}",
        )
