from django.urls import path, include 
from . import views

urlpatterns = [
    path("upload_data/", views.upload_data, name="upload_data"),
    # path("login/", ),
    path("/", include("django.contrib.auth.urls"),views.login_view, name="login"),
]
