from django.test import TestCase
from ..models import Book

class BookTest(TestCase):
    """
     Test module for Book Model
    """

    def setUp(self):
        Book.objects.create(
                isbn='0618260307',  title='The Hobbit', author='J. R. R. Tolkien', publisher='Houghton Mifflin')

        Book.objects.create(
                isbn='0908606664', title='Slinky Malinki', author='Lynley Dodd', publisher='Mallinson Rendel')


    def test_book_author(self):
        hobbit_author = Book.objects.get(title='The Hobbit')
        malinki_author = Book.objects.get(title='Slinky Malinki')

        self.assertEqual(
                hobbit_author.get_author(), "The Hobbit is written by J. R. R. Tolkien.")

        self.assertEqual(
                malinki_author.get_author(), "Slinky Malinki is written by Lynley Dodd.")


