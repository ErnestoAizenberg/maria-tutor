from django.urls import path
from django.contrib.sitemaps.views import sitemap
from main.sitemaps import StaticSitemap, ArticleSitemap

sitemaps = {
    'static': StaticSitemap,
    'articles': ArticleSitemap,
}

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("robots.txt", views.robots_txt),
    path("article/<slug:slug>/", views.article, name="article"),  # SEO-friendly URL
    path("articles/", views.articles, name="articles"),
    path("reviews/", views.reviews, name="reviews"),
    path("test1/", views.test, name="test"),
    path("success/", views.apply_success, name="apply_success"),
    path("application/", views.application, name="application"),
    path("apply/", views.application_submit, name="application_submit"),
    path("subscribe_email/", views.subscribe_email, name="subscribe_email"),
    path(
        "email_subscribe_success/",
        views.email_subscribe_success,
        name="email_subscribe_success",
    ),
    path("connect_request/", views.connect_request, name="connect_request"),
    path("connect_success/", views.connect_success, name="connect_success"),
    path("lessons/", views.lessons, name="lessons"),
    path("lessons2/", views.lessons2, name="lessons2"),
    path("about_me/", views.about_me, name="about_me"),
    path("science/", views.science, name="science"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
]

urlpatterns += [
    path('lessons-details/', views.lesson_details, name='lessons_details')
]
urlpatterns += [
    path('policy/', views.policy, name='policy'),
    path('terms/', views.terms, name='terms'),

]

urlpatterns += [
    path('programs/async/', views.async_program, name='async-program'),
    path('programs/bio-in-english/', views.bio_in_english, name='bio-in-english'),
    path('programs/groups/', views.group_programs, name='group-programs'),
    path('programs/olympiad-prep/', views.olympiad_prep, name='olympiad-prep'),
    path('programs/one-on-one/', views.one_on_one, name='one-on-one'),
    path('programs/subsized/', views.subsidized, name='subsized'),
]


