from django.urls import path

from . import views
from .views import IndexView, detail, vote


urlpatterns = [

    # /polls
    # path("", views.index),
    path("", IndexView.as_view(), name="index"),

    # /polls/5
    path("<int:question_id>/", views.detail, name="detail"),

    # /polls/5/vote
    path("<int:question_id>/vote/", views.vote, name="vote"),
]