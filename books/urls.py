from django.urls import path
from . import views 


urlpatterns = [
    path('', views.BooksListView.as_view(), name='book_list'),
    path('books/<int:pk>/', views.book_detail_view, name='book_detail'),
    path('new/', views.BooksCreateView.as_view(), name='book_create'),
    path('books/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
]