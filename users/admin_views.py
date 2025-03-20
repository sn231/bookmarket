from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from .models import User
from books.models import Book, Order
from orders.models import Order as OrderModel
from django.utils import timezone

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin()

class AdminDashboardView(AdminRequiredMixin, ListView):
    template_name = 'users/admin/dashboard.html'
    context_object_name = 'stats'

    def get_queryset(self):
        return {
            'total_users': User.objects.filter(role='user').count(),
            'total_books': Book.objects.count(),
            'total_orders': OrderModel.objects.count(),
            'pending_orders': OrderModel.objects.filter(status='pending').count(),
            'recent_users': User.objects.filter(role='user').order_by('-date_joined')[:5],
            'recent_orders': OrderModel.objects.order_by('-created_at')[:5],
        }

class UserManagementView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'users/admin/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.filter(role='user').order_by('-date_joined')

class UserUpdateView(AdminRequiredMixin, UpdateView):
    model = User
    template_name = 'users/admin/user_form.html'
    fields = ['username', 'email', 'phone', 'wechat', 'student_id', 'is_active']
    success_url = reverse_lazy('users:admin_user_list')

    def form_valid(self, form):
        messages.success(self.request, '用户信息更新成功！')
        return super().form_valid(form)

class UserDeleteView(AdminRequiredMixin, DeleteView):
    model = User
    template_name = 'users/admin/user_confirm_delete.html'
    success_url = reverse_lazy('users:admin_user_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, '用户已成功删除！')
        return super().delete(request, *args, **kwargs)

class OrderManagementView(AdminRequiredMixin, ListView):
    model = OrderModel
    template_name = 'users/admin/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return OrderModel.objects.all().order_by('-created_at')

class OrderUpdateView(AdminRequiredMixin, UpdateView):
    model = OrderModel
    template_name = 'users/admin/order_form.html'
    fields = ['status']
    success_url = reverse_lazy('users:admin_order_list')

    def form_valid(self, form):
        order = form.save(commit=False)
        if order.status == 'shipped':
            order.shipped_at = timezone.now()
        order.save()
        messages.success(self.request, '订单状态更新成功！')
        return super().form_valid(form)

class BookManagementView(AdminRequiredMixin, ListView):
    model = Book
    template_name = 'users/admin/book_list.html'
    context_object_name = 'books'

    def get_queryset(self):
        return Book.objects.all().order_by('-created_at')

class BookUpdateView(AdminRequiredMixin, UpdateView):
    model = Book
    template_name = 'users/admin/book_form.html'
    fields = ['title', 'author', 'price', 'condition', 'description', 'is_sold']
    success_url = reverse_lazy('users:admin_book_list')

    def form_valid(self, form):
        messages.success(self.request, '书籍信息更新成功！')
        return super().form_valid(form)

class BookDeleteView(AdminRequiredMixin, DeleteView):
    model = Book
    template_name = 'users/admin/book_confirm_delete.html'
    success_url = reverse_lazy('users:admin_book_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, '书籍已成功删除！')
        return super().delete(request, *args, **kwargs) 