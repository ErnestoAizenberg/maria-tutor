from django.contrib.auth import get_user_model
from django.core.validators import (EmailValidator, MaxValueValidator,
                                    MinValueValidator)
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

User = get_user_model()


class Review(models.Model):
    # Основная информация об авторе отзыва
    author_name = models.CharField(
        max_length=100,
        verbose_name="Имя автора",
        help_text="Как представиться автору отзыва (например: Анна К.)",
    )

    # Информация о достижениях/результатах (для подтверждения отзыва)
    achievement = models.CharField(
        max_length=200,
        verbose_name="Достижение/результат",
        help_text="Например: ЕГЭ по биологии, 98 баллов",
        blank=True,
        null=True,
    )

    # Основной текст отзыва
    content = models.TextField(
        verbose_name="Текст отзыва", help_text="Содержание отзыва"
    )

    # Оценка (если нужна рейтинговая система)
    """rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оценка",
        help_text="Оценка от 1 до 5",
        blank=True,
        null=True,
    )"""

    # Дата отзыва (автоматически устанавливается при создании)
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Дата создания"
    )

    # Статус отзыва (чтобы скрывать непроверенные отзывы)
    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликовано",
        help_text="Отображать ли отзыв на сайте",
    )

    # Дополнительные поля для SEO и админки
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name="URL-идентификатор",
        help_text="Уникальная часть URL для этого отзыва",
        blank=True,
    )

    # Сортировка (если нужно управлять порядком отзывов)
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок сортировки",
        help_text="Чем больше число, тем выше отзыв в списке",
    )

    author_photo = models.ImageField(
        upload_to='reviews/avatars/',
        blank=True,
        null=True,
        verbose_name="Фото автора"
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-order", "-created_at"]

    def __str__(self):
        return f"Отзыв от {self.author_name} ({self.created_at.date()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            # Создаем slug из имени и даты, если он не задан
            base_slug = f"{self.author_name}-{self.created_at.date()}"
            self.slug = slugify(base_slug)
        super().save(*args, **kwargs)


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
