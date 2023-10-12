from django.urls import path, include
from ki import views as kiViews
from django.contrib import admin  # Import admin module

urlpatterns = [
    path('ki/', include('ki.urls')),
    path('admin/', admin.site.urls),  # Add this line for the admin URL
    # ... Other URLs for your app ...
]
