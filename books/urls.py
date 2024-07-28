from django.urls import path
from . import views 


urlpatterns = [
    path('', views.BooksListView.as_view(), name='book_list'),
    path('<int:pk>/', views.BooksDetailView.as_view(), name='book_detail'),
    path('new/', views.BooksCreateView.as_view(), name='book_create'),
    path('<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_update'),
    path('<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
]