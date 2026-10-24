from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("menu/", views.menu_view, name="menu"),
    path("order/", views.place_order_view, name="place_order"),
    path("logout/", views.logout_view, name="logout"),
]