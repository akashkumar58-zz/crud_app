import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Book
from ..serializers import BookSerializer

#initialize the APIClient app

client = Client()

class GetAllBooksTest(TestCase):
    """
        Test module for GET all book API
    """
    def setUp(self):
        Book.objects.create(isbn='0618260307',  title='The Hobbit', author='J. R. R. Tolkien', publisher='Houghton Mifflin')
        Book.objects.create(isbn='0908606664', title='Slinky Malinki', author='Lynley Dodd', publisher='Mallinson Rendel')
        Book.objects.create(isbn='0704566664', title='A Song of Ice and Fire', author='George R. R. Martin', publisher='Bantam Books')


    def test_get_all_books(self):
        # get API response
        response = client.get(reverse('get_post_books'))
        # get data from database
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetSingleBookTest(TestCase):
    """
        Test module for GET single book API.
    """
    def setUp(self):
        self.hobbit = Book.objects.create(isbn='0618260307',  title='The Hobbit', author='J. R. R. Tolkien', publisher='Houghton Mifflin')
        self.slinky = Book.objects.create(isbn='0908606664', title='Slinky Malinki', author='Lynley Dodd', publisher='Mallinson Rendel')
        self.ice = Book.objects.create(
                isbn='0704566664', title='A Song of Ice and Fire', author='George R. R. Martin', publisher='Bantam Books')
        self.lotr = Book.objects.create(
                isbn='7357450150', title='The Fellowship of the Ring', author='J. R. R. Tolkien', publisher='Allen & Unwin')

    def test_get_valid_single_book(self):
        response = client.get(reverse('get_delete_update_book', kwargs={'pk': self.lotr.pk}))
        book = Book.objects.get(pk=self.lotr.pk)
        serializer = BookSerializer(book)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalide_single_book(self):
        response = client.get(reverse('get_delete_update_book', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CreateNewBookTest(TestCase):
    """
        Test module for inserting a new book in table.
    """
    def setUp(self):
        self.valid_payload = {
                'isbn': '0618260307',
                'title': 'The Hobbit',
                'author': 'J. R. R. Tolkien',
                'publisher': 'Allen & Unwin'
            }
        self.invalid_payload = {
                'isbn': '',
                'title': 'Godan',
                'author': 'Munshi Prechand',
                'publisher': 'Diamond Books'
            }

        def test_create_valid_payload(self):
            response = client.post(reverse('get_post_books'), data=json.dumps(self.valid_payload), content_type='application/json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        def test_create_invalid_payload(self):
            response = client.post(reverse('get_post_books'), data=json.dumps(self.invalid_payload), content_type='application/json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateSingleBookTest(TestCase):
    """
        Test module for updating an existing book
    """
    def setUp(self):
        self.lotr = Book.objects.create(
                isbn='7357450150', title='The Fellowship of the Ring', author='J. R. R. Tolkien', publisher='Allen & Unwin')
        self.godan = Book.objects.create(
                isbn='0123456789', title='Godan', author='Premchand', publisher='Diamond')

        self.valid_payload = {
            'isbn': '1234567890',
            'title': 'Godan',
            'author': 'Munshi Prechand',
            'publisher': 'Diamond Books'
        }

        self.invalid_payload = {
            'isbn': '',
            'title': 'The Fellowship of the Ring',
            'author': 'J. R. R. Tolkien',
            'publisher': 'Allen & Unwin'
        }


    def test_valid_update_book(self):
        response = client.put(
            reverse('get_delete_update_book', kwargs={'pk': self.godan.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_book(self):
        response = client.put(
            reverse('get_delete_update_book', kwargs={'pk': self.godan.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleBookTest(TestCase):
    """
        Test module to delete a single record of book.
    """
    def setUp(self):
        self.lotr = Book.objects.create(
                isbn='7357450150', title='The Fellowship of the Ring', author='J. R. R. Tolkien', publisher='Allen & Unwin')

    def test_valid_delete_book(self):
        response = client.delete(reverse('get_delete_update_book', kwargs={'pk': self.lotr.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_book(self):
        response = client.delete(reverse('get_delete_update_book', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

