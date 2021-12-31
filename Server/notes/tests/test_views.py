from django.test import TestCase


class NoteViewsTestCase(TestCase):
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
