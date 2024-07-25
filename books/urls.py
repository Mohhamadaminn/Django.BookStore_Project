from django.urls import path
from . import views 


urlpatterns = [
    path('', views.BooksListViews.as_view(), name='book_list_view'),
]