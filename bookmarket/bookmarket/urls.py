from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('books.urls')),
    path('users/', include('users.urls')),
    path('messages/', include('user_messages.urls', namespace='messages')),
    path('orders/', include('orders.urls')),
    path('', RedirectView.as_view(url='/books/', permanent=True)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 