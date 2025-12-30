import json
import logging

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage, send_mail
from django.core.validators import validate_email
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator

from .forms import ApplicationForm, ReviewForm, TutorConsultationForm
from .models import Application, Article, Publication, Review, Tag, LessonCard, ConnectMessage, TutorConsultationRequest, get_teacher
from .utils import search_models

logger = logging.getLogger('main')

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


def terms(request):
    context = {}
    return render(request, "main/terms.html", context)


def policy(request):
    context = {}
    return render(request, "main/policy.html", context)


def search_view(request):
    query = request.GET.get('q', '').strip()
    model_names = request.GET.getlist('models')

    if not model_names:
        model_names = ['main.Ativle', 'main.Review']

    results = []
    if query:
        results = search_models(query, model_names)

    # Пагинация
    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'results': page_obj,
        'page_obj': page_obj,
        'query': query,
        'model_names': model_names,
        'results_count': len(results),
    }
    logger.debug(f"Search page context: {context}")
    return render(request, 'main/search_results.html', context)

def index(request):
    """Display the homepage with published articles and application form."""

    try:
        # Get published articles ordered by creation date (newest first)
        articles = Article.objects.filter(status="published").order_by("-created_at")[:6]
        reviews = Review.objects.filter(is_published=True).order_by("-created_at")[:6]
        publications = Publication.objects.all()[:6]

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
            "publications": publications,
            "lesson_cards": LessonCard.objects.all(),
        }
        logger.debug(f"Main page context: {context}")

        if form.errors:
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
    teacher = get_teacher()
    page = teacher.get_page("lessons")
    context = {
        "lesson_cards": LessonCard.objects.all(),
        "page": page,
    }

    return render(request, "main/lessons.html", context)


def about_me(request):
    """Display about me page"""

    teacher = get_teacher()
    publications = Publication.objects.all()
    page = teacher.get_page("about_me")
    print(f"{page.name} sections: {page.sections}, page.config: {page.config}")

    context = {"page": page, "publications": publications}
    return render(request, "main/about_me.html", context)


def science(request):
    """Display science page"""
    publications = Publication.objects.all()
    context = {"publications": publications}

    return render(request, "main/science.html", context)

def articles_by_tag(request, slug):
    """Display list of articles by given slug of a tag"""
    logger.debug(f"loading articles by teg slug: {slug}")
    try:
        tag = get_object_or_404(Tag, slug=slug)
        logger.debug(f"found tag with this slug {tag}")
    except Exception as e:
        logger.error(f"Unexpexted error ocured while searching for tag: {str(e)}")
    try:
        articles_list = Article.objects.filter(
           tags=tag,
           status="published",
        ).select_related('author').prefetch_related('tags').order_by('-created_at')
        logger.debug(f"loaded list of articles for the tag: {articles_list}")
    except Exception as e:
        logger.error(f"An error occured while retring articles_list {str(e)}")

    try:
        paginator = Paginator(articles_list, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except Exception as e:
        logger.error(f"while trying to paginate: {str(e)}")

    context = {
        'tag': tag,
        'articles': page_obj,
        'page_title': f'Статьи на тему {tag.name}'
    }
    logger.debug(f"request context at articles_by_tag: {context}")

    try:
        page = render(request, 'main/articles_by_tag.html', context)
    except Exception as e:
        logger.error(f"While rendering articles_by_tag page an error occured: {str(e)}")
        raise

    return page


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
        logger.error(f"Error loading article {slug}: {str(e)}")
        messages.error(request, "Article could not be loaded")
        return redirect("index")


def articles(request):
    """Display a list of all published articles"""

    teacher = get_teacher()
    page = teacher.get_page("articles")

    try:
        list_articles = Article.objects.filter(status="published").order_by(
            "-created_at"
        )
        logger.debug(f"Found {len(list_articles)} published articles")
        return render(request, "main/articles.html", {"articles": list_articles, "page": page})
    except Exception as e:
        logger.error(f"Error loading articles list: {str(e)}", exc_info=True)
        messages.error(request, "Could not load articles")
        return render(request, "main/articles.html", {"articles": [], "page": page})


def test(request):
    """Route for testing templates"""
    return render(request, "main/article0.html")


def contacts(request):
    teacher = get_teacher()
    page = teacher.get_page("contacts")
    context = {"page": page}
    return render(request, "main/contacts.html", context)


def reviews(request):
    """Display a list of all published articles"""
    teacher = get_teacher()
    page = teacher.get_page("reviews")
    reviews = Review.objects.filter(is_published=True).order_by("-created_at")
    if "review_form_data" in request.session:
        form = ReviewForm(request.session["review_form_data"])

        # Add form errors from session if they exist
        if errors_json := request.session.get("review_form_errors"):
            errors_dict = json.loads(errors_json)
            for field, error_list in errors_dict.items():
                for error in errors_dict:
                    form.add_error(field, error)
                    messages.error(request, error)
        # Clean up session data
        request.session.pop("review_form_data", None)
        request.session.pop("review_form_errors", None)
    else:
        form = ReviewForm()

    context = {
        "reviews": reviews,
        "form": form,
        # "review_form": form,
    }
    logger.debug(f"Loaded {len(reviews)} published reviews for reviews page")
    return render(request, "main/reviews.html", context)


def add_review(request):
    if request.method != "POST":
        logger.error(f"Invalid HTTP method recieved in add_review: {request.method}")


    form = ReviewForm(
        request.POST,
        request.FILES,
    )
    if not form.is_valid():
        logger.warning(
            "Invalid application form submission", extra={"errors": form.errors}
        )
        request.session["review_form_data"] = request.POST
        request.session["review_form_errors"] = form.errors.as_json()

        return redirect("/reviews#review-form")

    review = form.save(commit=False)
    review.is_published = False  # Отзыв не будет опубликован сразу
    review.save()
    messages.success(
        request, "Спасибо за ваш отзыв! Он будет проверен администратором."
    )
    return redirect("/reviews#review-form")


def review_success(request):
    return render(request, "reviews/review_success.html")


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

        return redirect("application")

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
        try:
            email.send(fail_silently=False)
        except Exception as err:
            logger.error(f"While sending APPLICATION /email an error occured: {err}")

        try:
            application = Application(name=name, email=email, subject=subject, goal=goal)
            application.save()
        except Exception as e:
            logger.error(f"Failed to save Application, error: {str(e)}", exc_info=True)
            return HttpResponse(
                "Приносим извинения! Возникла техническая ошибка при отправке формы.<br><br>"
                "Мы уже получили уведомление о проблеме и работаем над её решением.<br>"
                "Вы можете:<ul>"
                "<li>Попробовать отправить заявку ещё раз через 5-10 минут</li>"
                "<li>Позвонить нам по телефону: +79213301390</li>"
                "<li>Написать на почту: sereernest@gmail.com</li></ul>", status=500)

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

    try:
        new_connect_msg = ConnectMessage(
            name=name,
            email=email,
            message=message,
        )
        new_connect_msg.save()
    except Exception as e:
        logger.error(f"Failed to save ConnectMessage, error: {str(e)}", exc_info=True)
        return HttpResponse(
            "Приносим извинения! Возникла техническая ошибка при отправке формы.<br><br>"
            "Мы уже получили уведомление о проблеме и работаем над её решением.<br>"
            "Вы можете:<ul>"
            "<li>Попробовать отправить заявку ещё раз через 5-10 минут</li>"
            "<li>Позвонить нам по телефону: +79213301390</li>"
            "<li>Написать на почту: sereernest@gmail.com</li></ul>", status=500)


    subject = f"Вопрос от {name}"
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email="noreply@yourdomain.com",  # Your verified sender
        to=["sereernest@gmail.com"],  # Recipient list
        reply_to=[email],  # Replies go to applicant
    )
    try:
        email.send(fail_silently=False)
    except Exception as err:
        logger.error(f"While CONTACT email an error occured: {err}")

    # Here you would typically save the message or send email
    logger.info("Contact form processed successfully")
    return redirect("connect_success")


def connect_success(request):
    """Display success page after contact form submission"""
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
    return render(request, "main/email_subscribe_success.html")


def async_program(request):
    return render(request, "main/programs/async.html")


def bio_in_english(request):
    return render(request, "main/programs/bio_on_english.html")


def group_programs(request):
    return render(request, "main/programs/grops.html")


def olympiad_prep(request):
    return render(request, "main/programs/olimp.html")


def one_on_one(request):
    return render(request, "main/programs/one_on_one.html")


def subsidized(request):
    return render(request, "main/programs/subsized.html")


def lesson_details(request):
    return render(request, "main/lessons_details.html")


def application(request):
    '''Aplication form display'''
    teacher = get_teacher()
    
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

    reviews = teacher.reviews.filter(
        is_published=True
    ).order_by('-order', '-created_at')[:3]
    
    context = {
        "application_form": form,
        "reviews": reviews,
    }
    return render(request, "main/application.html", context)


def tutor_consultation(request):
    """Display tutor consultation service page"""
    teacher = get_teacher()
    reviews = Review.objects.filter(is_published=True).order_by("-created_at")[:6]

    # Initialize form with session data if exists, otherwise create empty form
    if "consultation_form_data" in request.session:
        form = TutorConsultationForm(request.session["consultation_form_data"])

        # Add form errors from session if they exist
        if errors_json := request.session.get("consultation_form_errors"):
            errors_dict = json.loads(errors_json)
            for field, error_list in errors_dict.items():
                for error in error_list:
                    form.add_error(field, error)
                    messages.error(request, error)

        # Clean up session data
        request.session.pop("consultation_form_data", None)
        request.session.pop("consultation_form_errors", None)
    else:
        form = TutorConsultationForm()

    context = {
        "teacher": teacher,
        "reviews": reviews,
        "form": form,
    }
    return render(request, "main/services/tutor_consultation.html", context)


def tutor_consultation_submit(request):
    """Handle tutor consultation form submissions"""
    if request.method != "POST":
        logger.warning("Tutor consultation form submission attempted with non-POST method")
        return redirect("tutor_consultation")

    form = TutorConsultationForm(request.POST)

    if not form.is_valid():
        logger.warning(
            "Invalid tutor consultation form submission",
            extra={"errors": form.errors}
        )
        request.session["consultation_form_data"] = request.POST.dict()
        request.session["consultation_form_errors"] = form.errors.as_json()
        return redirect("tutor_consultation")

    try:
        name = form.cleaned_data.get("name", "").strip()
        user_email = form.cleaned_data.get("email", "").strip()
        phone = form.cleaned_data.get("phone", "").strip()
        question = form.cleaned_data.get("question", "").strip()
        experience_years = form.cleaned_data.get("experience_years")

        logger.info(f"Processing tutor consultation request from {name} <{user_email}>")

        # Save to database
        try:
            consultation_request = TutorConsultationRequest(
                name=name,
                email=user_email,
                phone=phone,
                question=question,
                experience_years=experience_years
            )
            consultation_request.save()
            logger.info(f"Tutor consultation request saved successfully (ID: {consultation_request.id})")
        except Exception as e:
            logger.error(f"Failed to save TutorConsultationRequest, error: {str(e)}", exc_info=True)
            messages.error(request, "Произошла ошибка при отправке заявки. Пожалуйста, попробуйте позже.")
            return redirect("tutor_consultation")

        # Send email notification
        subject = f"Заявка на консультацию для репетиторов от {name}"
        email_body = f"""
Новая заявка на консультацию для репетиторов:

Имя: {name}
Email: {user_email}
Телефон: {phone if phone else 'Не указан'}
Опыт работы: {experience_years if experience_years else 'Не указан'} лет

Вопрос/проблема:
{question}

---
ID заявки: {consultation_request.id}
Дата: {consultation_request.created_at.strftime('%Y-%m-%d %H:%M')}
        """

        email = EmailMessage(
            subject=subject,
            body=email_body,
            from_email="noreply@yourdomain.com",
            to=["sereernest@gmail.com"],
            reply_to=[user_email]
        )

        try:
            email.send(fail_silently=False)
            logger.info(f"Consultation request email sent successfully to sereernest@gmail.com")
        except Exception as err:
            logger.error(f"While sending consultation email an error occurred: {err}")

        messages.success(
            request,
            "Спасибо за вашу заявку! Я свяжусь с вами в течение 24 часов."
        )
        return redirect("tutor_consultation")

    except Exception as e:
        logger.error(f"Error processing tutor consultation request: {str(e)}", exc_info=True)
        messages.error(request, "Произошла ошибка при отправке заявки")
        return redirect("tutor_consultation")
