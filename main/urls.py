from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('article/<slug:slug>/', views.article, name='article'),  # SEO-friendly URL
    path('test1/', views.test, name='test'),
]
