from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("article/<slug:slug>/", views.article, name="article"),  # SEO-friendly URL
    path("articles/", views.articles, name="articles"),
    path("reviews/", views.reviews, name="reviews"),
    path("test1/", views.test, name="test"),
    path("success/", views.apply_success, name="apply_success"),
    path("apply/", views.application_submit, name="application_submit"),
    path("subscribe_email/", views.subscribe_email, name="subscribe_email"),
    path(
        "email_subscribe_success/",
        views.email_subscribe_success,
        name="email_subscribe_success",
    ),
    path("connect_request/", views.connect_request, name="connect_request"),
    path("connect_success/", views.connect_success, name="connect_success"),
]
