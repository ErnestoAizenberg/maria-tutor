import os

from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.html import format_html

from .custom_admin import custom_admin_site
from .models import Application, Article, Tag, ConnectMessage, Publication, Review, Teacher, LessonCard, LessonFeature


User = get_user_model()

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'truncated_content', 'rating', 'source', 'author_photo_url', 'is_published', 'created_at', 'order', 'preview_photo')
    list_editable = ('rating', 'is_published', 'order', 'author_photo_url', 'created_at')
    list_filter = ('is_published', 'rating', 'created_at', 'source')
    search_fields = ('author_name', 'content', 'achievement')
    actions = [
        'publish_selected',
        'unpublish_selected',
        'set_source_avito',
        'set_source_profi',
        'set_source_repetitor_ru',
        ]

    save_on_top = True

    fieldsets = (
        ('Основная информация', {
            'fields': ('author_name', 'author_photo_url', 'source', 'source_url', 'achievement', 'content', 'rating', 'created_at')
        }),
        ('Настройки публикации', {
            'fields': ('is_published', 'order', 'slug'),
            'classes': ('collapse',)
        }),
    )

    def truncated_content(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    truncated_content.short_description = 'Текст отзыва'

    def preview_photo(self, obj):
        if obj.author_photo_url:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.author_photo_url)
        return "-"
    preview_photo.short_description = 'Фото'

    def publish_selected(self, request, queryset):
        queryset.update(is_published=True)
    publish_selected.short_description = "Опубликовать выбранные отзывы"

    def unpublish_selected(self, request, queryset):
        queryset.update(is_published=False)
    unpublish_selected.short_description = "Снять с публикации выбранные отзывы"

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('created_at', 'slug')
        return ()


    def set_source_profi(self, request, queryset):
        queryset.update(source='profi_ru')
    set_source_profi.short_description = "Установить Profi.ru"

    def set_source_avito(self, request, queryset):
        queryset.update(source='avito')
    set_source_avito.short_description = "Установить Авито"

    def set_source_repetitor_ru(self, request, queryset):
        queryset.update(source='repetitor_ru')

    set_source_repetitor_ru.short_description = "Установить Repetitor.ru"


    class Media:
        css = {
            'all': ('css/admin_reviews.css',) if os.path.exists('static/css/admin_reviews.css') else {}
        }


class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "subject",
        "created_at",
        "is_processed",
        "process_actions",
    )
    list_filter = ("subject", "is_processed", "created_at")
    search_fields = ("name", "email", "goal")
    list_editable = ("is_processed",)
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "name", "email", "subject", "goal")
    fieldsets = (
        ("Personal Information", {"fields": ("name", "email")}),
        ("Application Details", {"fields": ("subject", "goal")}),
        ("Status", {"fields": ("is_processed",)}),
        ("Metadata", {"fields": ("created_at",), "classes": ("collapse",)}),
    )

    def has_add_permission(self, request):
        return False  # Запрещаем добавление новых Application

    def process_actions(self, obj):
        if not obj.is_processed:
            process_url = f"/admin/main/application/{obj.id}/process/"
            return format_html(
                '<a class="button" href="{}">Mark Processed</a>&nbsp;'
                '<a class="button" href="mailto:{}">Reply</a>',
                process_url,
                obj.email,
            )
        return format_html(
            '<a class="button" href="mailto:{}">Reply</a>',
            obj.email,
        )

    process_actions.short_description = "Actions"

    class Media:
        css = {"all": ("admin/css/custom.css",)}


class ConnectMessageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "short_message",
        "created_at",
        "is_read",
        "message_actions",
    )
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "message")
    list_editable = ("is_read",)
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "name", "email", "message")

    def has_add_permission(self, request):
        return False  # Запрещаем добавление новых ConnectMessage

    def short_message(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message

    short_message.short_description = "Message Preview"

    def message_actions(self, obj):
        if not obj.is_read:
            mark_read_url = f"/admin/main/connectmessage/{obj.id}/mark_read/"
            return format_html(
                '<a class="button" href="mailto:{}">Reply</a>&nbsp;'
                '<a class="button" href="{}">Mark Read</a>',
                obj.email,
                mark_read_url,
            )
        return format_html(
            '<a class="button" href="mailto:{}">Reply</a>',
            obj.email,
        )

    message_actions.short_description = "Actions"

    class Media:
        css = {"all": ("admin/css/custom.css",)}


class PublicationAdmin(admin.ModelAdmin):
    list_display = ("title", "journal", "publication_date", "is_featured")
    list_filter = ("journal", "publication_date", "is_featured")
    search_fields = ("title", "description", "authors", "journal")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "publication_date"

    formfield_overrides = {
        models.DateField: {"widget": forms.DateInput(attrs={"type": "date"})},
    }

    fieldsets = (
        (None, {"fields": ("title", "slug", "authors", "description")}),
        (
            "Publication Details",
            {"fields": ("journal", "publication_date", "doi", "url")},
        ),
        ("Metadata", {"fields": ("is_featured",)}),
    )


class ArticleAdminForm(forms.ModelForm):
    content = forms.CharField(
        widget=CKEditorWidget(config_name="default"), label="Контент"
    )  # Добавляем CKEditor для поля content

    # Кастомная форма с улучшенным виджетом для тегов
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple("Теги", False),
        required=False,
    )

    class Meta:
        model = Article
        fields = '__all__'

class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = (
        "title",
        "author",
        "status",
        "created_at",
        "updated_at",
        "image_preview_display",
        "display_tags",  # Новое поле для отображения тегов
    )
    list_filter = (
        "status",
        "created_at",
        "author",
        "tags",  # Добавляем фильтр по тегам
    )
    search_fields = (
        "title",
        "abstract",
        "content",
        "tags__name",  # Поиск по названиям тегов
    )
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at", "image_preview_display")
    filter_horizontal = ('tags',)  # Горизонтальный фильтр для тегов

    fieldsets = (
        (None, {"fields": ("title", "slug", "status", "author")}),
        ("Content", {"fields": ("abstract", "content", "image_preview", "tags")}),  # Добавили tags
        ("Dates", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def display_tags(self, obj):
        """Кастомное отображение тегов в списке статей"""
        return ", ".join([tag.name for tag in obj.tags.all()])
    display_tags.short_description = "Теги"

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "tags":
            kwargs["queryset"] = Tag.objects.order_by('name')
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def image_preview_display(self, obj):
        if obj.image_preview:
            return format_html(
                '<img src="{}" style="max-height: 100px;"/>',
                obj.image_preview.url
            )
        return "-"
    image_preview_display.short_description = "Preview"


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'article_count', 'created_at')
    search_fields = ('name', 'slug')
    list_filter = ('created_at',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'slug')
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def article_count(self, obj):
        return obj.article_set.count()
    article_count.short_description = "Кол-во статей"


class TeacherAdmin(admin.ModelAdmin):
    # Поля для отображения в списке
    list_display = (
        'name',
        'status',
        'email',
        'phone',
        'is_active',
        'avatar_preview',
        'created_at',
    )

    # Поля для поиска
    search_fields = (
        'name',
        'email',
        'phone',
        'status',
        'slug',
    )

    # Фильтры справа
    list_filter = (
        'is_active',
        'created_at',
    )

    # Поля только для чтения
    readonly_fields = (
        'slug',
        'created_at',
        'updated_at',
        'avatar_preview',
        'social_links',
    )

    # Группировка полей в форме редактирования
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'name',
                'status',
                'description',
                'is_active',
            )
        }),
        ('Контактная информация', {
            'fields': (
                'email',
                'phone',
            )
        }),
        ('Социальные сети', {
            'fields': (
                'telegram',
                'vk',
                'instagram',
                'twitter',
                'linkedin',
                'social_links',
            )
        }),
        ('Медиа', {
            'fields': (
                'avatar',
                'avatar_preview',
            )
        }),
        ('Мета', {
            'fields': (
                'lang',
                'keywords',
            ),
        }),
        #('Служебная информация', {
        #    'fields': (
        #        'slug',
        #        'created_at',
        #        'updated_at',
        #    )
        #}),"""
    )

    # Автоматическое заполнение slug при добавлении
    #prepopulated_fields = {'slug': ('name',)}

    # Сортировка по умолчанию
    ordering = ('-is_active', 'name')

    # Действия для списка
    actions = ['make_active', 'make_inactive']

    # Поля, которые можно редактировать прямо в списке
    list_editable = ('is_active',)

    # Пагинация
    list_per_page = 25

    # Кастомные методы
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.avatar.url
            )
        return "-"
    avatar_preview.short_description = 'Превью'

    def social_links(self, obj):
        links = []
        if obj.telegram:
            links.append(f'<a href="https://t.me/{obj.telegram}" target="_blank">Telegram</a>')
        if obj.vk:
            links.append(f'<a href="https://vk.com/{obj.vk}" target="_blank">VK</a>')
        if obj.instagram:
            links.append(f'<a href="https://instagram.com/{obj.instagram}" target="_blank">Instagram</a>')
        if obj.twitter:
            links.append(f'<a href="https://twitter.com/{obj.twitter}" target="_blank">Twitter</a>')
        if obj.linkedin:
            if obj.linkedin.startswith('http'):
                links.append(f'<a href="{obj.linkedin}" target="_blank">LinkedIn</a>')
            else:
                links.append(f'<a href="https://linkedin.com/in/{obj.linkedin}" target="_blank">LinkedIn</a>')

        return format_html(' | '.join(links)) if links else "-"
    social_links.short_description = 'Ссылки на соцсети'
    social_links.allow_tags = True

    # Кастомные действия
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Активировать выбранных учителей"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = "Деактивировать выбранных учителей"


class LessonFeatureInline(admin.TabularInline):
    model = LessonFeature
    extra = 1

class LessonCardAdmin(admin.ModelAdmin):
    list_display = ["title", "price", "order"]
    inlines = [LessonFeatureInline]
    list_editable = ["order"]


# Регистрация моделей в кастомной админке
custom_admin_site.register(User)
custom_admin_site.register(Teacher, TeacherAdmin)
custom_admin_site.register(LessonCard, LessonCardAdmin)
custom_admin_site.register(Application, ApplicationAdmin)
custom_admin_site.register(ConnectMessage, ConnectMessageAdmin)
custom_admin_site.register(Publication, PublicationAdmin)
custom_admin_site.register(Article, ArticleAdmin)
custom_admin_site.register(Tag, TagAdmin)
custom_admin_site.register(Review, ReviewAdmin)

# Настройки заголовков
custom_admin_site.site_header = "👾 Site Administration"
custom_admin_site.site_title = "👾 Site Admin Portal"
custom_admin_site.index_title = "👾 Site Admin"
