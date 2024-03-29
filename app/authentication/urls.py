from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import include
from django.urls import reverse_lazy
from .views import sign_out


app_name = "authentication"

urlpatterns = [
    path("signin", views.signin, name="signin"),
    path("register", views.register, name="register"),
    path("recover", views.recover, name="recover"),
    path('logout', sign_out, name='logout'),

]