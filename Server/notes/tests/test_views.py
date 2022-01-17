from accounts.tests.test_views import CreateCustomerViews
from change_log.models import ChangeLog
from datetime import datetime
from django.test import TestCase
from notes.tests.test_models import create_note


class NoteViewsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def setUp(self):
        pass

    def test_update_note(self):
        """
        Saves original value to change log and updates note
        """
        c = CreateCustomerViews()
        c.create_user()
        c.login()

        note = create_note(text="Test note.", user=c.user)

        data = dict(note="Test note!")

        res = c.client.patch(
            path=f"/notes/{note.id}/update",
            data=data,
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 200, f"Expected 200. Got {res.status_code}")
        self.assertNotEqual(
            res.data["note"], "Test note.", "Updated note matched previous value"
        )
        self.assertEqual(
            res.data["note"], "Test note!", "Updated note did not match expected value"
        )
        self.assertEqual(res.data["id"], note.id, "Reference Note PK mis-match")

        # Check that previous values were properly saved to the change log
        change_log = ChangeLog.objects.first()

        self.assertEqual(
            change_log.reference_model, "Notes", "Wrong reference table name"
        )
        self.assertEqual(res.data["id"], change_log.model_id, "Incorrect PK reference")
        self.assertEqual(
            change_log.field_name, "note", "Did not save the correct field name"
        )
        self.assertEqual(
            change_log.previous_value,
            "Test note.",
            "Did not correctly save the previous note",
        )
        self.assertEqual(
            change_log.previous_value_type,
            "str",
            "Did not dected the previous value as a string",
        )
        self.assertEqual(
            change_log.previous_user,
            note.user,
            "Change not associated with correct user",
        )
