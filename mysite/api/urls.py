from django.urls import path

from . import views

app_name = "api"
urlpatterns = [
    path("user/register", views.register, name="register"),
    path("user/login", views.login, name="login"),
    path("post", views.post, name="post"),
    path("post/<int:postid>", views.post_detail, name="post_detail"),
    path("comment/<int:postid>", views.comment, name="comment"),
]