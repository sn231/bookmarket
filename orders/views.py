from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from .models import Order, OrderItem
from books.models import CartItem
from django.http import JsonResponse

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user)

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user)

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.warning(request, '购物车是空的')
        return redirect('books:cart')

    if request.method == 'POST':
        try:
            with transaction.atomic():
                # 创建订单
                order = Order.objects.create(
                    buyer=request.user,
                    total_amount=sum(item.get_total_price() for item in cart_items),
                    payment_method=request.POST.get('payment_method'),
                    shipping_address=request.POST.get('shipping_address'),
                    contact_phone=request.POST.get('contact_phone'),
                    remarks=request.POST.get('remarks', '')
                )

                # 创建订单项
                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        book=cart_item.book,
                        book_title=cart_item.book.title,
                        price=cart_item.book.price,
                        quantity=cart_item.quantity
                    )
                    # 更新书籍库存
                    if not cart_item.book.update_stock(cart_item.quantity):
                        raise Exception(f'《{cart_item.book.title}》库存不足')

                # 清空购物车
                cart_items.delete()

                messages.success(request, '订单创建成功！')
                return redirect('orders:order_detail', pk=order.pk)

        except Exception as e:
            messages.error(request, f'创建订单失败：{str(e)}')
            return redirect('books:cart')

    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'total_amount': sum(item.get_total_price() for item in cart_items)
    })

@login_required
def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk, buyer=request.user)
    if order.status == 'pending':
        order.status = 'cancelled'
        order.cancelled_at = timezone.now()
        order.save()
        
        # 恢复库存
        for item in order.items.all():
            if item.book:
                item.book.stock += item.quantity
                item.book.save()
        
        messages.success(request, '订单已取消')
    else:
        messages.error(request, '只能取消待付款的订单')
    return redirect('orders:order_detail', pk=pk)

@login_required
def pay_order(request, pk):
    order = get_object_or_404(Order, pk=pk, buyer=request.user)
    if order.status != 'pending':
        messages.error(request, '订单状态不正确')
        return redirect('orders:order_detail', pk=pk)

    # 这里应该集成实际的支付系统
    # 目前仅作为演示，直接标记为已支付
    order.status = 'paid'
    order.paid_at = timezone.now()
    order.save()
    
    messages.success(request, '支付成功！')
    return redirect('orders:order_detail', pk=pk)

@login_required
def confirm_receipt(request, pk):
    order = get_object_or_404(Order, pk=pk, buyer=request.user)
    if order.status == 'shipped':
        order.status = 'completed'
        order.completed_at = timezone.now()
        order.save()
        messages.success(request, '已确认收货')
    else:
        messages.error(request, '只能确认已发货的订单')
    return redirect('orders:order_detail', pk=pk)
