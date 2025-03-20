from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Book, CartItem
from user_messages.models import Message
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Book.objects.filter(is_sold=False)
        q = self.request.GET.get('q')
        condition = self.request.GET.get('condition')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(author__icontains=q) |
                Q(description__icontains=q)
            )
        
        if condition:
            queryset = queryset.filter(condition=condition)
            
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
            
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
            
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conditions'] = Book.CONDITION_CHOICES
        return context

class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_books'] = Book.objects.filter(
            is_sold=False,
            seller=self.object.seller
        ).exclude(id=self.object.id)[:4]
        if self.request.user.is_authenticated:
            context['message_history'] = Message.objects.filter(
                book=self.object,
                sender__in=[self.request.user, self.object.seller],
                receiver__in=[self.request.user, self.object.seller]
            ).order_by('created_at')
        return context

class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    template_name = 'books/book_form.html'
    fields = ['title', 'author', 'price', 'original_price', 'condition', 'description', 'image']
    success_url = reverse_lazy('books:book_list')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        messages.success(self.request, '书籍发布成功！')
        return super().form_valid(form)

class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    template_name = 'books/book_form.html'
    fields = ['title', 'author', 'price', 'original_price', 'condition', 'description', 'image']

    def get_success_url(self):
        messages.success(self.request, '书籍信息更新成功！')
        return reverse_lazy('books:book_detail', kwargs={'pk': self.object.pk})

class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books:book_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, '书籍已成功删除！')
        return super().delete(request, *args, **kwargs)

def search_books(request):
    query = request.GET.get('q', '')
    if len(query) > 1:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query)
        )[:5]
        results = [{
            'id': book.id,
            'title': book.title,
            'price': str(book.price),
            'image': book.image.url if book.image else ''
        } for book in books]
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})

def load_more_books(request):
    page = request.GET.get('page', 1)
    books = Book.objects.filter(is_sold=False).order_by('-created_at')
    paginator = Paginator(books, 12)
    try:
        books_page = paginator.page(page)
    except:
        return JsonResponse({'books': []})
    
    books_data = [{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'price': str(book.price),
        'condition': book.get_condition_display(),
        'image': book.image.url if book.image else ''
    } for book in books_page]
    
    return JsonResponse({'books': books_data})

class MyBooksView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/my_books.html'
    context_object_name = 'books'

    def get_queryset(self):
        return Book.objects.filter(seller=self.request.user).order_by('-created_at')

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        book=book,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    cart_count = request.user.cart_items.count()
    return JsonResponse({
        'status': 'success',
        'message': '已添加到购物车',
        'cart_count': cart_count
    })

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return JsonResponse({
        'status': 'success',
        'message': '已从购物车移除'
    })

@login_required
def update_cart_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0 and quantity <= cart_item.book.stock:
        cart_item.quantity = quantity
        cart_item.save()
        return JsonResponse({
            'status': 'success',
            'total_price': str(cart_item.get_total_price())
        })
    return JsonResponse({
        'status': 'error',
        'message': '无效的数量'
    })

class CartView(LoginRequiredMixin, ListView):
    template_name = 'books/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_price = sum(item.get_total_price() for item in context['cart_items'])
        context['total_price'] = total_price
        return context 