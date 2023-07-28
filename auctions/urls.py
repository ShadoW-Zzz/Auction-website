from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:listing_id>", views.list, name="list"),
    path("categorydisplay", views.disp_category, name="categories"),
    path("addwatchlist/<int:listing_id>", views.add_watchlist, name = "watchlist"),
    path("removewatchlist/<int:listing_id>", views.remove_watchlist, name = "remove_watchlist"),
    path("displaywatch/", views.disp_watchlist , name="display_watchlist"),
    path("comments/<int:listing_id>", views.comment, name="comments")
]
