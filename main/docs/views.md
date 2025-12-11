Views.py Documentation

Practical reference for the tutoring website views

Overview

This Django views file handles all page rendering and form processing for a tutoring/education website. Organized by functionality with consistent error handling and logging.

Quick Navigation

Core Pages

View URL Pattern Purpose Key Features
index / Homepage Articles, reviews, application form, publications
lessons /lessons/ Lessons page Lesson cards, teacher page config
about_me /about_me/ About page Teacher info, publications
science /science/ Science page Publications list
articles /articles/ All articles Published articles list
article /articles/<slug>/ Single article Reading time, related articles
reviews /reviews/ Reviews page Published reviews, add review form
contacts /contacts/ Contact page Teacher contact info

Form Handlers

View Method Purpose Success Redirect
application_submit POST Tutoring application apply_success
add_review POST Add new review /reviews#review-form
connect_request POST Contact form connect_success
tutor_consultation_submit POST Tutor consultation tutor_consultation

Utility Pages

View Purpose Notes
search_view Site-wide search Paginated results, multi-model
articles_by_tag Filter articles by tag Paginated, tag-specific
robots_txt SEO robots.txt Custom allow/disallow rules

Design Patterns

1. Form Handling with Session Fallback

```python
# Common pattern for form error persistence
if "form_data" in request.session:
    form = FormClass(request.session["form_data"])
    # Restore errors from session
    request.session.pop("form_data", None)
else:
    form = FormClass()
```

2. Error Handling & Logging

```python
try:
    # Operation
except Exception as e:
    logger.error(f"Context: {str(e)}", exc_info=True)
    messages.error(request, "User-friendly message")
    # Fallback or redirect
```

3. Pagination Pattern

```python
paginator = Paginator(queryset, 10)
page_number = request.GET.get('page')
page_obj = paginator.get_page(page_number)
context = {'items': page_obj}
```

Key Components

Models Used

· Article - Blog articles with tags
· Review - Student/parent testimonials
· Publication - Academic publications
· Application - Tutoring applications
· TutorConsultationRequest - Tutor consultation requests
· ConnectMessage - General contact messages

Forms

· ApplicationForm - Student application
· ReviewForm - Add review
· TutorConsultationForm - Tutor consultation

Utils

· search_models() - Generic search across models
· get_teacher() - Get teacher profile with page configs

Common Tasks & Solutions

Adding a New Page

1. Add view function with teacher.get_page("page_name") if using teacher config
2. Create template in templates/main/
3. Add URL pattern in urls.py
4. Configure page in admin if using teacher page system

Adding Search to a Model

1. Ensure model has searchable fields
2. Update search_models() call in search_view to include model
3. Template displays results automatically

Creating a Form Handler

```python
def handle_form(request):
    if request.method != "POST":
        return redirect("form_page")
    
    form = FormClass(request.POST)
    if not form.is_valid():
        # Store in session for error display
        request.session["form_data"] = request.POST
        request.session["form_errors"] = form.errors.as_json()
        return redirect("form_page")
    
    # Process and save
    form.save()
    messages.success(request, "Success message")
    return redirect("success_page")
```

Email Sending Pattern

```python
email = EmailMessage(
    subject=f"Subject from {name}",
    body=message_content,
    from_email="noreply@domain.com",
    to=["recipient@email.com"],
    reply_to=[user_email]  # Important for replies
)
email.send(fail_silently=False)
```

Performance Tips

1. Use select_related and prefetch_related for foreign key relationships
2. Paginate lists with more than 10 items
3. Cache static pages like about_me, policy, terms
4. Lazy load images in article/content-heavy pages

Debugging

Log Locations

· Application errors: logger.error() with exc_info=True
· Form validation: logger.warning() with form errors
· Success actions: logger.info() for tracking

Common Issues

· Missing session cleanup: Always pop() session data after use
· Email failures: Check fail_silently=False in development
· Template errors: Check logger.debug() context output

Security Notes

1. POST-only for form submissions
2. Email validation with validate_email()
3. XSS protection: Django templates auto-escape
4. CSRF protection: Django middleware enabled
5. SQL injection: Use ORM, not raw queries

Maintenance Checklist

When updating views:

· Update logging context
· Test form validation messages
· Verify email templates
· Check pagination with edge cases
· Test session cleanup
· Update this documentation

Quick Reference

```python
# Get teacher/page config
teacher = get_teacher()
page = teacher.get_page("page_name")

# Get published articles
articles = Article.objects.filter(status="published").order_by("-created_at")

# Handle form with session persistence
if form.is_valid():
    # Process
else:
    request.session["form_data"] = request.POST
    request.session["form_errors"] = form.errors.as_json()

# Calculate reading time (words per minute)
reading_time = f"{word_count // 200} мин чтения"
```

---

Last updated with all views as of current implementation