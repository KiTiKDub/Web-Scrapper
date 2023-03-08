from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("log", views.log, name='log'),
    path("likes", views.likes, name="likes"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    #API
    path("history/<int:query_id>", views.history, name='history'),
    path("likes", views.likes, name='likes')

]