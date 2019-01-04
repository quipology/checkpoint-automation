from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('', include('create_object.urls')),
]

admin.site.site_header = 'Admin'
admin.site.site_title = 'Admin Portal'
admin.site.index_title = 'Welcome to xxxDigital CheckPoint Tool'