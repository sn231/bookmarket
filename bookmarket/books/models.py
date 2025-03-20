from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='分类名称')
    slug = models.SlugField(unique=True, verbose_name='URL别名')
    
    class Meta:
        verbose_name = '图书分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Book(models.Model):
    CONDITION_CHOICES = [
        ('new', '全新'),
        ('like_new', '九成新'),
        ('good', '良好'),
        ('acceptable', '可接受'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='书名')
    author = models.CharField(max_length=100, verbose_name='作者')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='分类')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='价格')
    original_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='原价')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, verbose_name='成色')
    description = models.TextField(verbose_name='描述')
    image = models.ImageField(upload_to='books/', verbose_name='图片')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='books', verbose_name='卖家')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    is_sold = models.BooleanField(default=False, verbose_name='是否已售')
    views = models.PositiveIntegerField(default=0, verbose_name='浏览次数')
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favorite_books', blank=True, verbose_name='收藏者')
    stock = models.PositiveIntegerField(default=1, verbose_name='库存数量')

    class Meta:
        verbose_name = '二手书'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def update_stock(self, quantity):
        if self.stock >= quantity:
            self.stock -= quantity
            self.save()
            return True
        return False

class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments', verbose_name='书籍')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='评论者')
    content = models.TextField(verbose_name='评论内容')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='评分'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', '待付款'),
        ('paid', '已付款'),
        ('shipped', '已发货'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]

    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', verbose_name='买家')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='书籍')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='订单状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    shipping_address = models.TextField(verbose_name='收货地址')
    payment_method = models.CharField(max_length=50, verbose_name='支付方式')
    transaction_id = models.CharField(max_length=100, blank=True, verbose_name='交易号')

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_items', verbose_name='用户')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='书籍')
    quantity = models.PositiveIntegerField(default=1, verbose_name='数量')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '购物车项'
        verbose_name_plural = verbose_name
        unique_together = ['user', 'book']

    def get_total_price(self):
        return self.book.price * self.quantity

class UserProfile(models.Model):
    CREDIT_CHOICES = [
        ('excellent', '优秀'),
        ('good', '良好'),
        ('fair', '一般'),
        ('poor', '较差'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name='头像')
    credit_score = models.CharField(max_length=20, choices=CREDIT_CHOICES, default='good', verbose_name='信用评分')
    bio = models.TextField(blank=True, verbose_name='个人简介')
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followers', blank=True, verbose_name='关注')

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = verbose_name 