from accounts.tests.test_models import CreateUser
from django.test import TestCase
from os.path import join as os_join
from pathlib import Path

SAMPLE_FILE_DIR = os_join(Path(__file__).resolve().parent, "sample_files")


class DocumentsModelsTestCase(TestCase):
    """
    Tests the companies model for errors
    """

    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def setUp(self):
        pass


class ImagesModelsTestCase(TestCase):
    """
    Tests the companies model for errors
    """

    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def setUp(self):
        pass
