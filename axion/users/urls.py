from django.urls import path
from . import views

urlpatterns = [
    path("<int:user_id>/", views.user_detail, name="user-detail"),
    path("login/", views.login_view),
    path("signup/", views.signup_view),
]
