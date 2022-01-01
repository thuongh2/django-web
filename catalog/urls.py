from django.urls import path
from django.urls.conf import re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('books/', views.BookListView.as_view(), name='books'),
    path('authors/', views.AuthorsListView.as_view(), name='authors'),

    re_path(r'^book/(?P<pk>\d+)$', views.book_detail_view.as_view(), name='book-detail'),
    re_path(r'^author/(?P<pk>\d+)$', views.author_detail_view.as_view(), name='author-detail'),

    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.LoanedBookListView.as_view(), name='borrowed'),

    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

urlpatterns += [
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]

urlpatterns += [
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
]