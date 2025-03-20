from django.urls import path
from . import views

app_name = 'messages'

urlpatterns = [
    path('', views.MessageListView.as_view(), name='message_list'),
    path('send/<int:book_id>/', views.MessageCreateView.as_view(), name='message_create'),
    path('<int:pk>/mark_read/', views.mark_as_read, name='mark_read'),
] 