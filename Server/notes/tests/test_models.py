from django.test import TestCase
from accounts.tests.test_models import create_user_obj
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
        return Notes.objects.create(
            note=random_sentence(
                total_len=random_bell_curve_int(low=4, high=128), allow_numbers=True
            ),
            user=create_user_obj(),
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
        return Notes.objects.create(note=text, user=create_user_obj())

    # If all fields were passed
    return Notes.objects.create(note=text, user=user)


class NoteModelsTestCase(TestCase):
    """
    Test the notes model to check for errors.
    """

    @classmethod
    def setUpTestData(self) -> None:
        # print(
        #     "setUpTestData: Run once to set up non-modified data for all class methods."
        # )
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
        user = create_user_obj()
        note = create_note(text="Testing", user=user)
        self.assertEqual(note.user_id, user.id, "User ID mis-match on Note creation")
        self.assertEqual(note.note, "Testing", "Note text mis-match on Note creation")
        self.assertIsNone(note.changed_to, "Value was not None")
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

    def test_current_note_deletion_previous_note_remains(self):
        """
        Tests that when the current note is deleted that the previous note remains.
        """
        note_1 = create_note()
        note_2 = create_note()
        note_1.changed_to = note_2
        note_1.save()
        note_2.save()
        note_2.delete()
        self.assertEqual(
            Notes.objects.all().count(),
            0,
            f"Expected 0 notes, found {Notes.objects.all().count()}",
        )

    def test_original_note_deletion_removes_linked_note(self):
        """
        Tests that when the previous note is deleted that the current note is removed too.
        """
        note_1 = create_note()
        note_2 = create_note()
        note_1.changed_to = note_2
        note_1.save()
        note_2.save()
        note_1.delete()
        self.assertEqual(
            Notes.objects.all().count(),
            1,
            f"Expected 1 note, found {Notes.objects.all().count()}",
        )

    def test_original_note_deletion_removes_all_linked_notes(self):
        """
        Tests that when the previous note is deleted that the current note is removed too.
        """
        note_1 = create_note()
        note_2 = create_note()
        note_3 = create_note()
        note_1.changed_to = note_2
        note_2.changed_to = note_3
        note_1.save()
        note_2.save()
        note_3.save()
        note_1.delete()
        self.assertEqual(
            Notes.objects.all().count(),
            2,
            f"Expected 2 notes, found {Notes.objects.all().count()}",
        )
