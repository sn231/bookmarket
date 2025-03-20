from django.db import models
from django.conf import settings
from books.models import Book

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', '待付款'),
        ('paid', '已付款'),
        ('shipped', '已发货'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]

    PAYMENT_CHOICES = [
        ('alipay', '支付宝'),
        ('wechat', '微信支付'),
        ('bank', '银行转账'),
    ]

    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders_orders', verbose_name='买家')
    order_number = models.CharField(max_length=20, unique=True, verbose_name='订单编号')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='订单状态')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总金额')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, verbose_name='支付方式')
    shipping_address = models.TextField(verbose_name='收货地址')
    contact_phone = models.CharField(max_length=15, verbose_name='联系电话')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')
    shipped_at = models.DateTimeField(null=True, blank=True, verbose_name='发货时间')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    cancelled_at = models.DateTimeField(null=True, blank=True, verbose_name='取消时间')
    remarks = models.TextField(blank=True, verbose_name='备注')

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'订单号: {self.order_number}'

    def generate_order_number(self):
        import time
        return f"BO{int(time.time())}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='订单')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, verbose_name='书籍')
    book_title = models.CharField(max_length=200, verbose_name='书籍标题')  # 冗余存储，防止书籍被删除
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='单价')
    quantity = models.PositiveIntegerField(default=1, verbose_name='数量')

    class Meta:
        verbose_name = '订单项'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.book_title} x {self.quantity}'

    def get_total_price(self):
        return self.price * self.quantity

class Transaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='transactions', verbose_name='订单')
    transaction_id = models.CharField(max_length=100, unique=True, verbose_name='交易号')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='交易金额')
    payment_method = models.CharField(max_length=20, verbose_name='支付方式')
    status = models.CharField(max_length=20, verbose_name='交易状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')

    class Meta:
        verbose_name = '交易记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'交易号: {self.transaction_id}'
