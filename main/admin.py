# main/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.html import format_html

from .custom_admin import custom_admin_site
from .models import Application, Article, ConnectMessage, Review

User = get_user_model()


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

from django import forms
from ckeditor.widgets import CKEditorWidget

class ArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config_name='default'), label="Контент")  # Добавляем CKEditor для поля content

    class Meta:
        model = Article
        fields = '__all__'

class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm  # Используем кастомную форму с CKEditor
    list_display = ("title", "author", "status", "created_at", "updated_at", "image_preview_display")
    list_filter = ("status", "created_at", "author")
    search_fields = ("title", "abstract", "content")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at", "image_preview_display")
    fieldsets = (
        (None, {"fields": ("title", "slug", "status", "author")}),
        ("Content", {"fields": ("abstract", "content", "image_preview")}),
        ("Dates", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def image_preview_display(self, obj):
        if obj.image_preview:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image_preview.url)
        return "-"

    image_preview_display.short_description = "Preview"

# Регистрация моделей в кастомной админке
custom_admin_site.register(User)
custom_admin_site.register(Application, ApplicationAdmin)
custom_admin_site.register(ConnectMessage, ConnectMessageAdmin)
custom_admin_site.register(Article, ArticleAdmin)
custom_admin_site.register(Review)

# Настройки заголовков
custom_admin_site.site_header = "Your Site Administration"
custom_admin_site.site_title = "Your Site Admin Portal"
custom_admin_site.index_title = "Welcome to Your Site Admin"
