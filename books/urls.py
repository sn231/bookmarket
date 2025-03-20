# books/urls.py
from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('create/', views.BookCreateView.as_view(), name='book_create'),
    path('<int:pk>/update/', views.BookUpdateView.as_view(), name='book_update'),
    path('<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
    path('my-books/', views.MyBooksView.as_view(), name='my_books'),
    path('search/', views.search_books, name='search_books'),
    path('load-more/', views.load_more_books, name='load_more_books'),
    
    # 修改购物车URL配置
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    
    # 库存管理
    path('<int:pk>/update-stock/', views.update_stock, name='update_stock'),
    # 其他路由...
]