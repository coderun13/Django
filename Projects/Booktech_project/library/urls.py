from django.urls import path
from . import views
from .views import BookDetailView, BookListView

urlpatterns = [
    # Function Based Views
    path('', views.book_list, name='book_list_fbv'),
    path('fbv/books/<int:book_id>/', views.book_detail, name='book_detail_fbv'),

    # Class Based Views
    path('cbv/books/', BookListView.as_view(), name='book_list_cbv'),
    path('cbv/books/<int:pk>/', BookDetailView.as_view(), name='book_detail_cbv'),
    path('authors/<int:author_id>/books/', views.books_by_author, name='books_by_author'),
    path('authors/', views.author_list, name='author_list'),
    path('book/add/', views.add_book, name='add_book'),
    path('book/add_with_author/', views.add_book_and_author, name='add_book_and_author'),
    path('publisher/add_book_with_author_publisher/', views.add_book_with_author_publisher, name='add_book_with_author_publisher'),
]