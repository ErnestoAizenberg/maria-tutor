from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator
from django.db import models
from django.utils.text import slugify

User = get_user_model()


class Application(models.Model):
    SUBJECT_CHOICES = [
        ("general", "General Inquiry"),
        ("partnership", "Partnership Opportunity"),
        ("career", "Career Opportunity"),
        ("other", "Other"),
    ]

    name = models.CharField(
        max_length=300,
        blank=False,
        verbose_name="Applicant Name",
        help_text="Full name of the applicant",
    )
    email = models.EmailField(
        max_length=300,
        blank=False,
        verbose_name="Email Address",
        help_text="Email address of the applicant",
        validators=[EmailValidator()],
    )
    goal = models.TextField(
        max_length=1200,
        blank=False,
        verbose_name="Applicant Goal",
        help_text="Detailed description of the applicant's goals",
    )
    subject = models.CharField(
        max_length=300,
        choices=SUBJECT_CHOICES,
        default="general",
        verbose_name="Subject",
        help_text="Category of the application",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
    )
    is_processed = models.BooleanField(
        default=False,
        verbose_name="Processed Status",
        help_text="Whether the application has been processed",
    )

    class Meta:
        verbose_name = "Application"
        verbose_name_plural = "Applications"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Application from {self.name} ({self.subject})"


class ConnectMessage(models.Model):
    name = models.CharField(
        max_length=300,
        blank=False,
        verbose_name="Sender Name",
        help_text="Full name of the message sender",
    )
    email = models.EmailField(
        max_length=300,
        blank=False,
        verbose_name="Email Address",
        help_text="Email address of the sender",
        validators=[EmailValidator()],
    )
    message = models.TextField(
        max_length=1200,
        blank=False,
        verbose_name="Message Content",
        help_text="Content of the message",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name="Read Status",
        help_text="Whether the message has been read",
    )

    class Meta:
        verbose_name = "Connection Message"
        verbose_name_plural = "Connection Messages"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"Message from {self.name} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"
        )


class Article(models.Model):
    # Basic fields
    title = models.CharField(max_length=200)
    abstract = models.CharField(
        max_length=300,
        blank=True,
        help_text="Brief summary (appears in article listings)",
    )
    content = models.TextField()

    # Auto-generated fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    # Relationships
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # Status
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.abstract and self.content:  # Auto-generate abstract if empty
            self.abstract = (
                self.content[:297] + "..." if len(self.content) > 300 else self.content
            )
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]
