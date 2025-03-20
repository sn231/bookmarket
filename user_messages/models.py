from django.db import models
from users.models import User
from books.models import Book

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name='发送者')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', verbose_name='接收者')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='messages', verbose_name='相关书籍')
    content = models.TextField(verbose_name='消息内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')
    is_read = models.BooleanField(default=False, verbose_name='是否已读')

    class Meta:
        verbose_name = '消息'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.sender} to {self.receiver}: {self.content[:20]}' 