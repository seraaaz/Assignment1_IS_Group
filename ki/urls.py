from django.urls import path
from . import views

urlpatterns = [
    path("upload_data/", views.upload_data, name="upload_data"),
    path("login/", views.login_view, name="login"),
    # Define URLs for other categories as needed.
]
