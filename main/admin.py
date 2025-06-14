from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'abstract', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('title', 'abstract', 'content')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'status')
        }),
        ('Content', {
            'fields': ('abstract', 'content'),
            'classes': ('wide',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ('created_at', 'updated_at')
