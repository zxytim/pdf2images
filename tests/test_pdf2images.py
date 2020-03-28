import unittest
import pdf2images
import os

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
ASSETS_DIR = os.path.join(THIS_DIR, "assets")


class TestPDF2Images(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdf_path = os.path.join(ASSETS_DIR, "Sequence Modeling 2019-04.pdf")
        with open(cls.pdf_path, "rb") as f:
            cls.pdf_data = f.read()

    def test_basics(self):
        self.assertEqual(pdf2images.get_num_pages_given_path(self.pdf_path), 175)
