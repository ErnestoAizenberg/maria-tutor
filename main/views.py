"""
Personal website for biology/chemistry tutor Maria Seredinskaya
"""

import json

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage, send_mail
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404, redirect, render

from tutorproject.logger import setup_logger

from .forms import ApplicationForm
from .models import Application, Article, Review

logger = setup_logger(log_file="app.log", level="DEBUG")
from django.http import HttpResponse

def robots_txt(request):
    content = """User-agent: *
    Allow: /$
    Allow: /about_me/
    Allow: /lessons/
    Allow: /science/
    Disallow: /admin/
    Disallow: /static/
    Sitemap: https://mariaseredinskaya.pythonanywhere.com/sitemap.xml"""
    return HttpResponse(content, content_type="text/plain")

def index(request):
    """Display the homepage with published articles and application form."""
    logger.info("Rendering homepage")

    try:
        # Get published articles ordered by creation date (newest first)
        articles = Article.objects.filter(status="published").order_by("-created_at")
        reviews = Review.objects.filter(is_published=True).order_by("-created_at")

        # Initialize form with session data if exists, otherwise create empty form
        if "application_form_data" in request.session:
            form = ApplicationForm(request.session["application_form_data"])

            # Add form errors from session if they exist
            if errors_json := request.session.get("application_form_errors"):
                errors_dict = json.loads(errors_json)
                for field, error_list in errors_dict.items():
                    for error in errors_dict:
                        form.add_error(field, error)

            # Clean up session data
            request.session.pop("application_form_data", None)
            request.session.pop("application_form_errors", None)
        else:
            form = ApplicationForm()

        context = {
            "articles": articles,
            "reviews": reviews,
            "application_form": form,
        }
        logger.debug(f"form.erros: {form.errors}")
        logger.debug(f"Loaded {len(articles)} published articles for homepage")
        return render(request, "main/index-purple.html", context)

    except Exception as e:
        logger.error(f"Error rendering homepage: {str(e)}", exc_info=True)
        messages.error(request, "An error occurred while loading the page")

        # Return empty context in case of error
        return render(
            request,
            "main/index-purple.html",
            {"articles": [], "application_form": ApplicationForm()},
        )

def lessons(request):
    """Display lessons page"""
    logger.info("Rendering lessons page")
    context = {}

    return render(request, "main/lessons.html", context)


def lessons2(request):
    """Display lessons page"""
    logger.info("Rendering lessons page")
    context = {}

    return render(request, "main/lessons1.html", context)


def about_me(request):
    """Display about me page"""
    logger.info("Rendering about me page")
    context = {}

    return render(request, "main/about_me.html", context)


def science(request):
    """Display science page"""
    logger.info("Rendering science page")
    context = {}

    return render(request, "main/science.html", context)


def article(request, slug):
    """Display a single article with reading time and related articles"""
    logger.info(f"Attempting to load article with slug: {slug}")
    try:
        article = get_object_or_404(Article, slug=slug, status="published")
        logger.debug(f"Found article: {article.title}")

        # Calculate reading time
        READING_SPEED = 200  # words per minute
        word_count = len(article.content.split())
        reading_time_minutes = max(1, round(word_count / READING_SPEED))
        reading_time = f"{reading_time_minutes} мин чтения"

        # Get related articles
        related_articles = (
            Article.objects.filter(status="published")
            .exclude(id=article.id)
            .order_by("-created_at")[:5]
        )
        logger.debug(f"Found {len(related_articles)} related articles")

        context = {
            "article": article,
            "reading_time": reading_time,
            "related_articles": related_articles,
        }
        return render(request, "main/article-purple.html", context)
    except Exception as e:
        logger.error(f"Error loading article {slug}: {str(e)}", exc_info=True)
        messages.error(request, "Article could not be loaded")
        return redirect("index")


def articles(request):
    """Display a list of all published articles"""
    logger.info("Loading all published articles")
    try:
        list_articles = Article.objects.filter(status="published").order_by(
            "-created_at"
        )
        logger.debug(f"Found {len(list_articles)} published articles")
        return render(request, "main/articles.html", {"articles": list_articles})
    except Exception as e:
        logger.error(f"Error loading articles list: {str(e)}", exc_info=True)
        messages.error(request, "Could not load articles")
        return render(request, "main/articles.html", {"articles": []})


def test(request):
    """Route for testing templates"""
    logger.debug("Test route accessed")
    return render(request, "main/article0.html")

def reviews(request):
    """Display a list of all published articles"""
    reviews = Review.objects.filter(is_published=True).order_by("-created_at")
    context = {
        "reviews": reviews,
        #"review_form": form,
    }
    logger.debug(f"Loaded {len(reviews)} published reviews for reviews page")
    return render(request, "main/reviews.html", context)


def application_submit(request):
    """Handle tutoring application submissions"""
    if request.method != "POST":
        logger.warning("Application submission attempted with non-POST method")
        form = ApplicationForm()
        return render(request, "main/index-purple.html", {"application_form": form})

    form = ApplicationForm(request.POST)
    if not form.is_valid():
        logger.warning(
            "Invalid application form submission", extra={"errors": form.errors}
        )
        request.session["application_form_data"] = request.POST
        request.session["application_form_errors"] = form.errors.as_json()

        return redirect("/#application-form")

    try:
        name = form.cleaned_data.get("name", "").strip()
        user_email = form.cleaned_data.get("email", "").strip()
        subject = form.cleaned_data.get("subject", "").strip()
        goal = form.cleaned_data.get("goal", "").strip()

        logger.info(f"Processing application from {name} <{user_email}> for {subject}")

        subject = (f"Запрос на обучение по <{subject}> от {name}",)
        message = goal

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email="noreply@yourdomain.com",  # Your verified sender
            to=["sereernest@gmail.com"],  # Recipient list
            reply_to=[user_email],  # Replies go to applicant
        )
        email.send(fail_silently=False)

        application = Application(name=name, email=email, subject=subject, goal=goal)
        application.save()
        logger.info(f"Application saved successfully (ID: {application.id})")

        return redirect("apply_success")

    except ValidationError:
        logger.warning(f"Invalid email address provided: {email}")
        messages.error(request, "Please enter a valid email address")
        return redirect("index")
    except Exception as e:
        logger.error(f"Error processing application: {str(e)}", exc_info=True)
        messages.error(request, "An error occurred while processing your application")
        return redirect("index")


def apply_success(request):
    """Display success page after application submission"""
    logger.info("Application success page accessed")
    return render(request, "main/apply_success.html")


def connect_request(request):
    """Handle contact form submissions"""
    if request.method != "POST":
        logger.warning("Contact form submission attempted with non-POST method")
        return redirect("index")

    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    message = request.POST.get("message", "").strip()

    logger.info(f"Contact request from {name} <{email}>")

    if not all([name, email, message]):
        logger.warning("Incomplete contact form submission")
        messages.error(request, "Please fill all form fields")
        return redirect("index")

    try:
        validate_email(email)
    except ValidationError:
        logger.warning(f"Invalid email in contact form: {email}")
        messages.error(request, "Please enter a valid email address")
        return redirect("index")

    subject = f"Вопрос от {name}"
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email="noreply@yourdomain.com",  # Your verified sender
        to=["sereernest@gmail.com"],  # Recipient list
        reply_to=[email],  # Replies go to applicant
    )
    email.send(fail_silently=False)

    # Here you would typically save the message or send email
    logger.info("Contact form processed successfully")
    return redirect("connect_success")


def connect_success(request):
    """Display success page after contact form submission"""
    logger.debug("Contact success page accessed")
    return render(request, "main/connect_success.html")


def subscribe_email(request):
    """Handle email newsletter subscriptions"""
    if request.method != "POST":
        logger.warning("Email subscription attempted with non-POST method")
        return redirect("index")

    email = request.POST.get("email", "").strip()
    logger.info(f"Email subscription attempt for: {email}")

    if not email:
        logger.warning("Empty email submission")
        messages.error(request, "Please enter an email address")
        return redirect("index")

    try:
        validate_email(email)
    except ValidationError:
        logger.warning(f"Invalid email in subscription: {email}")
        messages.error(request, "Please enter a valid email address")
        return redirect("index")

    # Here you would typically add to mailing list

    send_mail(
        "Subscription on Maria Tutor",
        "You have been subscribed.",
        "sereernest@gmail.com",
        [email],
        fail_silently=False,
    )
    logger.info(f"Email subscription successful for: {email}")
    return redirect("email_subscribe_success")


def email_subscribe_success(request):
    """Display success page after email subscription"""
    logger.debug("Email subscription success page accessed")
    return render(request, "main/email_subscribe_success.html")

def async_program(request):
    return render(request, 'main/programs/async.html')

def bio_in_english(request):
    return render(request, 'main/programs/bio_on_english.html')

def group_programs(request):
    return render(request, 'main/programs/grops.html')

def olympiad_prep(request):
    return render(request, 'main/programs/olimp.html')

def one_on_one(request):
    return render(request, 'main/programs/one_on_one.html')

def subsidized(request):
    return render(request, 'main/programs/subsized.html')

def lesson_details(request):
    return render(request, 'main/lessons_details.html')

def application(request):
    # Initialize form with session data if exists, otherwise create empty form
    if "application_form_data" in request.session:
        form = ApplicationForm(request.session["application_form_data"])

        # Add form errors from session if they exist
        if errors_json := request.session.get("application_form_errors"):
            errors_dict = json.loads(errors_json)
            for field, error_list in errors_dict.items():
                for error in errors_dict:
                    form.add_error(field, error)

        # Clean up session data
        request.session.pop("application_form_data", None)
        request.session.pop("application_form_errors", None)
    else:
        form = ApplicationForm()


    context = {
        "application_form": form,
    }
    return render(request, 'main/application.html', context)
