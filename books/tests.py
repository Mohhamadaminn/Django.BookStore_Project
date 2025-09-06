from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Book


class BookViewsTest(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')

        # Create a test book
        self.book = Book.objects.create(
            title='Test Book',
            author='John Doe',
            description='A test description',
            price=10.99
        )

    def test_book_list_view(self):
        """Book list view should load properly"""
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_book_detail_view(self):
        """Book detail view should display the book information"""
        response = self.client.get(reverse('book_detail', args=[self.book.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)
        self.assertTemplateUsed(response, 'books/book_detail.html')

    def test_book_create_view_redirect_if_not_logged_in(self):
        """If not logged in, user should be redirected when accessing book_create"""
        response = self.client.get(reverse('book_create'))
        self.assertNotEqual(response.status_code, 200)

    def test_book_create_view_logged_in(self):
        """Logged in user should be able to create a book"""
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('book_create'), {
            'title': 'New Book',
            'author': 'Jane Doe',
            'description': 'Another description',
            'price': 15.99
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful creation
        self.assertEqual(Book.objects.last().title, 'New Book')

    def test_book_update_view(self):
        """Logged in user should be able to update a book"""
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('book_update', args=[self.book.pk]), {
            'title': 'Updated Title',
            'author': 'John Doe',
            'description': 'Updated description',
            'price': 12.50
        })
        self.assertEqual(response.status_code, 302)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Title')

    def test_book_delete_view(self):
        """Logged in user should be able to delete a book"""
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('book_delete', args=[self.book.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Book.objects.filter(pk=self.book.pk).exists())
