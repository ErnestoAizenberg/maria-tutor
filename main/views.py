from django.shortcuts import render, get_object_or_404
from .models import Article


def index(request):
    articles = Article.objects.filter(status='published').order_by('-created_at')
    return render(request, 'main/index-m.html', {'articles': articles})

def article(request, slug):
    article = get_object_or_404(Article, slug=slug, status='published')
    reading_spead = 200
    word_count = len(article.content.split())
    reading_time_minutes = max(1, round(word_count / reading_spead))
    reading_time = f"{reading_time_minutes} мин чтения"

    return render(request, 'main/article.html', {'article': article, 'reading_time': reading_time})

def test(request):
    return render(request, 'main/article0.html')
