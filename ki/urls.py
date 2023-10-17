from django.urls import path, include
from . import views

urlpatterns = [
    path("upload_data/", views.upload_data, name="upload_data"),
    path("login/", views.login_view, name="login"),
    path("download_data/<str:file_type>/", views.download_data, name="download_data"),
    path("upload_success/", views.upload_success, name="upload_success"),
    path("profile/", views.profile, name="profile"),
]
