from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Book


class BookViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password123'
        )

        self.book = Book.objects.create(
            title='Test Book',
            author='John Doe',
            description='A test description',
            price=10.99,
            user=self.user
        )

    def test_book_list_view(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')

    def test_book_detail_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('book_detail', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')

    def test_book_create_view_logged_in(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('book_create'), {
            'title': 'New Book',
            'author': 'Jane Doe',
            'description': 'Another description',
            'price': 20.50,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.last().title, 'New Book')
        self.assertEqual(Book.objects.last().user, self.user)

    def test_book_create_view_not_logged_in(self):
        response = self.client.post(reverse('book_create'), {
            'title': 'Unauthorized Book',
            'author': 'Hacker',
            'description': 'Should not be created',
            'price': 15.00,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.count(), 1)

    def test_book_update_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('book_update', args=[self.book.id]), {
            'title': 'Updated Book',
            'author': 'John Doe',
            'description': 'Updated description',
            'price': 12.50,
        })
        self.assertEqual(response.status_code, 302)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')

    def test_book_delete_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('book_delete', args=[self.book.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.count(), 0)
