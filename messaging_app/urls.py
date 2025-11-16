from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/chats/', include('chats.urls')),  # future API endpoints for messages
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='chats-home'),
]
