from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('sending_messages.urls', namespace='sending_messages')),
    path('users/', include('users.urls', namespace='users')),

]
