from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    # Add other URLs for registration, login, etc.
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('books/', views.BookList.as_view(), name='books'),
    path('books/<int:pk>', views.BookDetail.as_view(), name='book'),
    path('books/add/', views.BookCreate.as_view(), name='book-create'),
    path('books/update/<int:pk>', views.BookUpdate.as_view(), name='book-update'),
    path('books/delete/<int:pk>', views.BookDelete.as_view(), name='book-delete'),
]
