from django.urls import path
from . import views

urlpatterns = [
    path('users', views.UserListView.as_view()),
    path('users/<int:pk>', views.UserDetailView.as_view()),
    path('books', views.BookListView.as_view()),
    path('books/<int:pk>', views.BookDetailView.as_view()),
    path('shops', views.ShopListView.as_view()),
    path('shops/<int:pk>', views.ShopDetailView.as_view()),
    path('cart', views.CartListView.as_view()),
    path('orders', views.OrderListView.as_view()),
    path('orders/<int:pk>', views.OrderDetailView.as_view()),
    path('order-items', views.OrderItemListView.as_view()),
    path('order-items/<int:pk>', views.OrderItemDetailView.as_view()),
]
