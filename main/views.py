from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404, redirect, render

from .models import Article

"""
Personal website for biology/chemistry tutor Maria Seredinskaya
"""


def index(request):
    """Display the homepage with published articles"""
    articles = Article.objects.filter(status="published").order_by("-created_at")
    return render(request, "main/index-purple.html", {"articles": articles})


def article(request, slug):
    """Display a single article with reading time and related articles"""
    article = get_object_or_404(Article, slug=slug, status="published")

    # Calculate reading time
    READING_SPEED = 200  # words per minute
    word_count = len(article.content.split())
    reading_time_minutes = max(1, round(word_count / READING_SPEED))
    reading_time = f"{reading_time_minutes} мин чтения"

    # Get related articles (excluding current article)
    related_articles = (
        Article.objects.filter(status="published")
        .exclude(id=article.id)
        .order_by("-created_at")[:5]
    )  # Limit to 5 most recent

    context = {
        "article": article,
        "reading_time": reading_time,
        "related_articles": related_articles,
    }
    return render(request, "main/article-purple.html", context)


def articles(request):
    """Display a list of all published articles"""
    list_articles = Article.objects.filter(status="published").order_by("-created_at")
    return render(request, "main/articles.html", {"articles": list_articles})


def test(request):
    """Route for testing templates"""
    return render(request, "main/article0.html")


# Application Form Handling
def application_submit(request):
    """Handle tutoring application submissions"""
    if request.method != "POST":
        return redirect("index")

    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    subject = request.POST.get("subject", "").strip()
    goal = request.POST.get("goal", "").strip()

    # Basic validation
    if not name or not email:
        messages.error(request, "Пожалуйста заполните все обязательные поля")
        return redirect("index")

    try:
        validate_email(email)
    except ValidationError:
        messages.error(request, "Пожалуйста введите корректный email адрес")
        return redirect("index")

    # Here you would typically save the application to a database
    # and/or send an email notification

    return redirect("apply_success")


def apply_success(request):
    """Display success page after application submission"""
    return render(request, "main/apply_success.html")


# Contact Form Handling
def connect_request(request):
    """Handle contact form submissions"""
    if request.method != "POST":
        return redirect("index")

    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    message = request.POST.get("message", "").strip()

    # Basic validation
    if not all([name, email, message]):
        messages.error(request, "Пожалуйста заполните все поля формы")
        return redirect("index")

    try:
        validate_email(email)
    except ValidationError:
        messages.error(request, "Пожалуйста введите корректный email адрес")
        return redirect("index")

    # Here you would typically save the message to a database
    # and/or send an email notification

    return redirect("connect_success")


def connect_success(request):
    """Display success page after contact form submission"""
    return render(request, "main/connect_success.html")


# Email Subscription Handling
def subscribe_email(request):
    """Handle email newsletter subscriptions"""
    if request.method != "POST":
        return redirect("index")

    email = request.POST.get("email", "").strip()

    if not email:
        messages.error(request, "Пожалуйста введите email адрес")
        return redirect("index")

    try:
        validate_email(email)
    except ValidationError:
        messages.error(request, "Пожалуйста введите корректный email адрес")
        return redirect("index")

    # Here you would typically add the email to your mailing list

    return redirect("email_subscribe_success")


def email_subscribe_success(request):
    """Display success page after email subscription"""
    return render(request, "main/email_subscribe_success.html")
