from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()

class Article(models.Model):
    # Basic fields
    title = models.CharField(max_length=200)
    abstract = models.CharField(
        max_length=300,
        blank=True,
        help_text="Brief summary (appears in article listings)"
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
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.abstract and self.content:  # Auto-generate abstract if empty
            self.abstract = self.content[:297] + '...' if len(self.content) > 300 else self.content
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
