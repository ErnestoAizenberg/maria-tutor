import os
import yaml

from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator, FileExtensionValidator, URLValidator, MinValueValidator, MaxValueValidator, ValidationError

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

User = get_user_model()

LANGUAGE_CHOICES = [
    ('ru', 'Russian'),
    ('en', 'English'),
]
def get_teacher():
    return Teacher.objects.filter(lang='ru').first()

class Teacher(models.Model):
    def upload_avatar(self, filename):
        """Генерирует путь для загрузки аватара учителя."""
        ext = filename.split(".")[-1].lower()
        return f"teacher/avatars/{self.name}.{ext}"

    # Основная информация
    name = models.CharField(
        max_length=100,
        blank=False,
        verbose_name="Имя",
        help_text="Полное имя учителя",
    )

    status = models.CharField(
        max_length=250,
        blank=False,
        verbose_name="Статус",
        help_text="Краткий статус под именем учителя",
    )

    description = models.TextField(
        max_length=800,
        blank=True,
        verbose_name="Описание",
        help_text="Подробное описание учителя",
    )

    avatar = models.ImageField(
        upload_to=upload_avatar,
        blank=True,
        null=True,
        verbose_name="Аватар",
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp"])
        ],
        help_text="Изображение должно быть в формате JPG, PNG или WEBP. Рекомендуемый размер: 300x300px.",
    )

    avatar2 = models.ImageField(
        upload_to=upload_avatar,
        blank=True,
        null=True,
        verbose_name="Второй аватар",
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp"])
        ],
        help_text="Изображение должно быть в формате JPG, PNG или WEBP. Рекомендуемый размер: 300x300px. Аватар для страницы about.",
    )
    # Контактная информация
    email = models.EmailField(
        max_length=300,
        blank=True,
        verbose_name="Email",
        help_text="Электронная почта учителя",
        validators=[EmailValidator()],
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Телефон",
        help_text="Контактный телефон учителя",
    )

    # Социальные сети
    telegram = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Telegram",
        help_text="Имя пользователя в Telegram (без @)",
    )

    vk = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="VK",
        help_text="Имя пользователя или ID в VK",
    )

    instagram = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Instagram",
        help_text="Имя пользователя в Instagram (без @)",
    )

    twitter = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Twitter",
        help_text="Имя пользователя в Twitter (без @)",
    )

    linkedin = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="LinkedIn",
        help_text="Имя пользователя или URL в LinkedIn",
    )

    # Служебные поля
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name="URL-идентификатор",
        help_text="Автоматическое поле для удобных URL",
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
        help_text="Отображается ли учитель на сайте",
    )

    lang = models.CharField(
        max_length=20,
        choices=LANGUAGE_CHOICES,
        default="en",
        verbose_name="Язык",
        help_text="Язык для которого учитель создаётся",
    )

    keywords = models.CharField(
        max_length=700,
        blank=True,
        null=True,
        verbose_name="Кей-слова",
        help_text="Ключевые слова для поиска",
    )

    education = models.JSONField(null=True, blank=True, verbose_name='Образование')
    scientific_work = models.JSONField(null=True, blank=True, verbose_name='Научная работа')
    tutoring = models.JSONField(null=True, blank=True, verbose_name='Репетиторство')

    @property
    def aggregate_rating(self):
        from django.db.models import Avg
        avg = self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']

        return round(avg, 1) if avg is not None else 0

    class Meta:
        verbose_name = "Учитель"
        verbose_name_plural = "Учителя"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.status}"

    def save(self, *args, **kwargs):
        if not self.slug:
            if not self.name:
                raise ValueError("Нельзя сгенерировать slug: необходимо указать имя учителя")

            base_slug = slugify(self.name)
            self.slug = base_slug

            # Проверка уникальности slug
            similar_slugs = set(
                Teacher.objects.filter(slug__startswith=base_slug)
                .exclude(pk=self.pk)
                .values_list("slug", flat=True)
            )

            if self.slug in similar_slugs:
                counter = 1
                while f"{base_slug}-{counter}" in similar_slugs:
                    counter += 1
                self.slug = f"{base_slug}-{counter}"

        super().save(*args, **kwargs)

    def get_page(self, page_slug):
        return self.pages.filter(slug=page_slug).first()

    def get_social_links(self):
        """Возвращает словарь с ссылками на социальные сети учителя."""
        socials = {}
        if self.telegram:
            socials['telegram'] = f"https://t.me/{self.telegram}"
        if self.vk:
            socials['vk'] = f"https://vk.com/{self.vk}"
        if self.instagram:
            socials['instagram'] = f"https://instagram.com/{self.instagram}"
        if self.twitter:
            socials['twitter'] = f"https://twitter.com/{self.twitter}"
        if self.linkedin:
            socials['linkedin'] = self.linkedin if self.linkedin.startswith('http') else f"https://linkedin.com/in/{self.linkedin}"
        return socials


class Page(models.Model):
    teacher = models.foreignkey(
        'teacher',
        on_delete=models.set_null,
        related_name='pages',
        null=true,
        blank=true,
    )
    name = models.CharField(
        max_length=200,
        help_text="Page name, displayed in footer and navbar"
    )
    show_in_navbar = models.BooleanField(default=False)
    show_in_footer = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)

    # SEO fields with more appropriate max_lengths
    title = models.CharField(max_length=200)
    meta_description = models.CharField(max_length=300, blank=True)
    meta_keywords = models.CharField(max_length=300, blank=True)

    # OpenGraph fields
    og_type = models.CharField(max_length=50, default='website', blank=True)
    og_site_name = models.CharField(max_length=100, blank=True)
    og_title = models.CharField(max_length=300, blank=True)
    og_description = models.CharField(max_length=500, blank=True)
    og_url = models.URLField(max_length=500, blank=True)
    og_image = models.URLField(max_length=500, blank=True)
    og_image_width = models.PositiveIntegerField(blank=True, null=True)
    og_image_height = models.PositiveIntegerField(blank=True, null=True)
    og_locale = models.CharField(max_length=10, default='en_US', blank=True)

    # Twitter fields
    twitter_card = models.CharField(max_length=50, default='summary_large_image', blank=True)
    twitter_title = models.CharField(max_length=300, blank=True)
    twitter_description = models.CharField(max_length=500, blank=True)
    twitter_image = models.URLField(max_length=500, blank=True)

    # Hero section
    hero_title = models.CharField(max_length=200, blank=True)
    hero_sub_title = models.CharField(max_length=400, blank=True)

    # URL and tracking
    slug = models.SlugField(
        max_length=200,
        unique=False,
        help_text="URL part after /, can be not unique",
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)

    config_yaml = models.TextField(blank=True, help_text="Конфигурация страницы в формате YAML")
    #_config_data = None

    @property
    def config(self):
        """
        Возвращает распаршенный конфиг.
        Всегда возвращает словарь, даже при ошибках.
        """
        try:
            if self.config_yaml.strip():
                parsed_config = yaml.safe_load(self.config_yaml) or {}
                print(f"DEBUG: Successfully parsed config for {self.slug}: {parsed_config}")  # ОТЛАДКА
                return parsed_config
            print(f"DEBUG: Empty config for {self.slug}")  # ОТЛАДКА
            return {}
        except yaml.YAMLError as e:
            print(f"DEBUG: YAML ERROR for {self.slug}: {e}")  # ОТЛАДКА
            print(f"DEBUG: Config content: {self.config_yaml}")  # ОТЛАДКА
            return {}
        except Exception as e:
            print(f"DEBUG: UNEXPECTED ERROR for {self.slug}: {e}")  # ОТЛАДКА
            return {}

    @property
    def sections(self):
        return self.config.get('sections', [])

    @property
    def cta(self):
        return self.config.get('cta', {})

    def __str__(self):
        return self.name

    def view(self):
        self.views += 1
        self.save(update_fields=['views'])

    class Meta:
        ordering = ['-created_at']


class TariffQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def with_format_groups(self):
        return self.order_by('format_type', 'program_name')

    def for_teacher(self, teacher):
        return self.active().filter(teacher=teacher)

class TariffManager(models.Manager):
    def get_queryset(self):
        return TariffQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def with_format_groups(self):
        return self.get_queryset().with_format_groups()

    def for_teacher(self, teacher):
        return self.get_queryset().for_teacher(teacher)


class Tariff(models.Model):
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='tariffs',
        null=True,
        blank=True,
    )
    format_type = models.CharField(
        max_length=50,
        verbose_name='Тип формата',
        help_text='Основной тип формата (Индивидуально/Парные/Групповые/Асинхронное)'
    )
    format_display = models.CharField(
        max_length=50,
        verbose_name='Отображаемое название формата',
        help_text='Как будет показано в таблице'
    )
    program_name = models.CharField(
        max_length=100,
        verbose_name='Название программы'
    )
    price = models.PositiveIntegerField(verbose_name='Стоимость')
    price_unit = models.CharField(
        max_length=20,
        default='₽/час',
        verbose_name='Единица стоимости'
    )
    is_group_format = models.BooleanField(
        default=False,
        verbose_name='Групповой формат?',
        help_text='Для стилизации групповых форматов'
    )

    # Метаданные
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(default=True)

    objects = TariffManager()

    class Meta:
        ordering = ['format_type', 'program_name']
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'
        indexes = [
            models.Index(fields=['format_type']),
            models.Index(fields=['is_active']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.teacher.name}-{self.format_type}-{self.program_name}")
            self.slug = base_slug
            counter = 1
            while Tariff.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.format_display} {self.program_name}: {self.price}{self.price_unit}"

class Review(models.Model):
    SOURCE_UNKNOWN = "unknown"
    SOURCE_NATIVE = "native"  # Оставлен напрямую на сайте
    SOURCE_PROFI_RU = "profi_ru"
    SOURCE_REPETITOR_RU = "repetitor_ru"
    SOURCE_GOOGLE = "google"
    SOURCE_YANDEX = "yandex"
    SOURCE_SOCIAL = "social"  # Соцсети (VK, Telegram и т.д.)
    SOURCE_OTHER = "other"  # Другой источник (свободный ввод)
    SOURCE_AVITO = "avito"

    SOURCE_CHOICES = [
        (SOURCE_UNKNOWN, "Неизвестно"),
        (SOURCE_NATIVE, "Нативный (с вашего сайта)"),
        (SOURCE_PROFI_RU, "Profi.ru"),
        (SOURCE_AVITO, "Авито"),
        (SOURCE_REPETITOR_RU, "Ваш репетитор"),
        (SOURCE_GOOGLE, "Google Отзывы"),
        (SOURCE_YANDEX, "Яндекс Услуги"),
        (SOURCE_SOCIAL, "Социальные сети"),
        (SOURCE_OTHER, "Другое"),
    ]

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reviews",
    )

    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        default=SOURCE_UNKNOWN,
        verbose_name="Источник отзыва",
        help_text="Откуда взят этот отзыв?",
    )

    # Если источник "other" — можно уточнить вручную
    source_custom = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        verbose_name="Уточнение источника",
        help_text="Например: Instagram, рекомендация друга и т.д.",
    )
    source_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на отзыв")

    # Основная информация об авторе отзыва
    author_photo_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Ссылка на фото автора",
        help_text="URL аватара (Например с Google, VK, Profi.ru и т.д.)",
    )
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

    # Оценка
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оценка",
        help_text="Оценка от 1 до 5",
        blank=True,
        null=True,
    )

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


    @property
    def model_verbose_name(self):
        return self._meta.verbose_name

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-order", "-created_at"]

    def __str__(self):
        return f"Отзыв от {self.author_name} ({self.created_at.date()})"

    def get_source_display(self):
        if self.source == self.SOURCE_OTHER and self.source_custom:
            return self.source_custom
        return dict(self.SOURCE_CHOICES).get(self.source, "Неизвестно")

    def save(self, *args, **kwargs):
        if not self.slug:
            if not self.author_name:
                raise ValueError("Cannot generate slug: author_name is required")

            base_slug = slugify(f"{self.author_name}-{self.created_at.date()}")
            self.slug = base_slug

            # Get all similar slugs at once
            similar_slugs = set(
                self.__class__.objects.filter(slug__startswith=base_slug)
                .exclude(pk=self.pk)
                .values_list("slug", flat=True)
            )

            if self.slug in similar_slugs:
                counter = 1
                while f"{base_slug}-{counter}" in similar_slugs:
                    counter += 1
                self.slug = f"{base_slug}-{counter}"

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

    @property
    def model_verbose_name(self):
        return self._meta.verbose_name

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

    @property
    def model_verbose_name(self):
        return self._meta.verbose_name

    class Meta:
        verbose_name = "Connection Message"
        verbose_name_plural = "Connection Messages"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"Message from {self.name} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"
        )


class Publication(models.Model):
    title = models.CharField(
        max_length=700,
        verbose_name="Publication Title",
        help_text="The full title of the publication",
    )

    slug = models.SlugField(
        max_length=700,
        unique=True,
        blank=True,
        help_text="A URL-friendly version of the title (auto-generated)",
    )

    authors = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Authors",
        help_text="List of authors separated by commas",
    )

    description = models.TextField(
        max_length=2000,
        blank=True,
        verbose_name="Abstract/Description",
        help_text="Brief summary or abstract of the publication",
    )

    url = models.URLField(
        max_length=500,
        validators=[URLValidator()],
        verbose_name="Publication URL",
        help_text="Link to the full publication",
    )

    journal = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Journal/Conference",
        help_text="Name of the journal or conference where published",
    )

    doi = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="DOI",
        help_text="Digital Object Identifier if available",
    )

    publication_date = models.DateField(
        verbose_name="Publication Date",
        help_text="Date when the publication was released",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    is_featured = models.BooleanField(
        default=False,
        verbose_name="Featured Publication",
        help_text="Mark as featured to highlight this publication",
    )

    @property
    def model_verbose_name(self):
        return self._meta.verbose_name

    class Meta:
        verbose_name = "Publication"
        verbose_name_plural = "Publications"
        ordering = ["-publication_date"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["publication_date"]),
            models.Index(fields=["is_featured"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:700]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("publication_detail", kwargs={"slug": self.slug})


class Tag(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название тега",
        help_text="Максимум 100 символов"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name="URL-имя",
        allow_unicode=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('articles_by_tag', kwargs={'slug': self.slug})

    def clean(self):
        # Запрещаем теги с одинаковым slug
        if Tag.objects.filter(slug=slugify(self.name)).exclude(id=self.id).exists():
            raise ValidationError("Тег с таким URL-именем уже существует")

class Article(models.Model):
    def upload_preview(self, filename):
        ext = filename.split(".")[-1]
        return f"articles/previews/{self.slug}.{ext}"

    # Basic fields
    title = models.CharField(max_length=200)
    abstract = models.CharField(
        max_length=300,
        blank=True,
        help_text="Brief summary (appears in article listings)",
    )
    content = models.TextField()

    image_preview = models.ImageField(
        upload_to=upload_preview,
        blank=True,
        null=True,
        verbose_name="Превью статьи",
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp"])
        ],
        help_text="Изображение должно быть в формате JPG, PNG или WEBP.",
    )

    # Auto-generated fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    # Relationships
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Tag)

    # Status
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk:
            old_article = Article.objects.get(pk=self.pk)
            if (
                old_article.image_preview
                and old_article.image_preview != self.image_preview
            ):
                if os.path.isfile(old_article.image_preview.path):
                    os.remove(old_article.image_preview.path)

        if not self.slug:
            self.slug = slugify(self.title)
        if not self.abstract and self.content:  # Auto-generate abstract if empty
            self.abstract = (
                self.content[:297] + "..." if len(self.content) > 300 else self.content
            )
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image_preview:
            if os.path.isfile(self.image_preview.path):
                os.remove(self.image_preview.path)
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("article", kwargs={"slug": self.slug})


    @property
    def model_verbose_name(self):
        return self._meta.verbose_name

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"


class LessonCard(models.Model):
    # Основные поля
    title = models.CharField("Название", max_length=100)  # "Индивидуальные занятия"
    icon_class = models.CharField("Иконка (Font Awesome)", max_length=50, default="fas fa-star")  # "fas fa-user-graduate"
    price = models.CharField("Цена", max_length=50)  # "от 1600 ₽/час"
    button_text = models.CharField("Текст кнопки", max_length=50, default="Подробнее")  # "Подробнее о тарифах"
    button_link = models.CharField("Ссылка кнопки", max_length=100, blank=True)  # "/programs/one-on-one"
    is_featured = models.BooleanField("Пометка 'ВЫГОДНО'", default=False)

    # Для удобного администрирования (необязательно)
    order = models.PositiveIntegerField("Порядок отображения", default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order"]


class LessonFeature(models.Model):
    card = models.ForeignKey(LessonCard, on_delete=models.CASCADE, related_name="features")
    text = models.CharField("Текст пункта", max_length=200)  # "Гибкое расписание"

    def __str__(self):
        return self.text
