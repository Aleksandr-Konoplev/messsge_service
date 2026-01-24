from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include(('sending_messages.urls', 'sending_messages'), namespace='sending_messages')),

]
