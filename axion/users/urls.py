from django.urls import path
from . import views

urlpatterns = [
    path("<int:user_id>/", views.user_detail, name="user-detail"),
    path("login/", views.login_view),
    path("logout/", views.logout_view),
    path("me/", views.me_view),
]
