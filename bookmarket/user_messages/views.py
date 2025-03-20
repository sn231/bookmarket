from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Message
from books.models import Book
from django.contrib import messages

class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messages/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user)

class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ['content']
    template_name = 'messages/message_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = get_object_or_404(Book, pk=self.kwargs['book_id'])
        return context

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.book = get_object_or_404(Book, pk=self.kwargs['book_id'])
        form.instance.receiver = form.instance.book.seller
        messages.success(self.request, '消息发送成功！')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('books:book_detail', kwargs={'pk': self.kwargs['book_id']})

@login_required
def mark_as_read(request, pk):
    message = get_object_or_404(Message, pk=pk, receiver=request.user)
    message.is_read = True
    message.save()
    messages.success(request, '消息已标记为已读')
    return redirect('messages:message_list') 