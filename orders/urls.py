from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order_list'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('<int:pk>/cancel/', views.cancel_order, name='cancel_order'),
    path('<int:pk>/pay/', views.pay_order, name='pay_order'),
    path('<int:pk>/confirm/', views.confirm_receipt, name='confirm_receipt'),
] 