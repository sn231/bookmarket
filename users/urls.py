from django.urls import path
from . import views
from . import admin_views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='users:login'), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    
    # 管理员URL
    path('admin/dashboard/', admin_views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin/users/', admin_views.UserManagementView.as_view(), name='admin_user_list'),
    path('admin/users/<int:pk>/update/', admin_views.UserUpdateView.as_view(), name='admin_user_update'),
    path('admin/users/<int:pk>/delete/', admin_views.UserDeleteView.as_view(), name='admin_user_delete'),
    path('admin/orders/', admin_views.OrderManagementView.as_view(), name='admin_order_list'),
    path('admin/orders/<int:pk>/update/', admin_views.OrderUpdateView.as_view(), name='admin_order_update'),
    path('admin/books/', admin_views.BookManagementView.as_view(), name='admin_book_list'),
    path('admin/books/<int:pk>/update/', admin_views.BookUpdateView.as_view(), name='admin_book_update'),
    path('admin/books/<int:pk>/delete/', admin_views.BookDeleteView.as_view(), name='admin_book_delete'),
] 