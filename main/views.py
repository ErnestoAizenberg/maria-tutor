from django.shortcuts import render, redirect, get_object_or_404
from .models import Article


def index(request):
    articles = Article.objects.filter(status='published').order_by('-created_at')
    return render(request, 'main/index-purple.html', {'articles': articles})

def article(request, slug):
    article = get_object_or_404(Article, slug=slug, status='published')
    related_articles = Article.objects.filter(status='published').order_by('-created_at')
    reading_spead = 200
    word_count = len(article.content.split())
    reading_time_minutes = max(1, round(word_count / reading_spead))
    reading_time = f"{reading_time_minutes} мин чтения"

    return render(request, 'main/article-purple.html', {'article': article, 'reading_time': reading_time, "related_articles": related_articles})

def articles(request):
    list_articles = Article.objects.filter(status='published').order_by('-created_at')
    return render(
        request,
        'main/articles.html',
        {'articles': list_articles}
    )


def test(request):
    return render(request, 'main/article0.html')

def apply_success(request):
    return render(request, 'main/apply_success.html')

def application_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        goal = request.POST.get('goal')

        if not name or not email:
            return render(request, 'index-purple.html', {'error': 'Пожалуйста заполните все поля(('})

        return redirect('apply_success')
    else:
        pass

def connect_request(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        return redirect('connect_success')
    else:
        pass

def connect_success(request):
    if request.method == 'GET':
        return render(request, 'main/connect_success.html')
    else:
        pass

def email_subscribe_success(request):
    return render(request, 'main/email_subscribe_success.html')

def subscribe_email(request):
    if request.method == 'POST':
        return redirect('email_subscribe_success')
