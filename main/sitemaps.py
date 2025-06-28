from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Article  # Import your Article model if you have one


class StaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8  # Default priority for all items

    def items(self):
        # List of view names to include in sitemap
        return [
            "index",
            "articles",
            "reviews",
            "lessons",
            "about_me",
            "science",
            "lessons_details",
            "terms",
            "policy",
            "subsized",
            "olympiad-prep",
            "subsized",
            "one-on-one",
            "group-programs",
            "async-program",
            # Excluded URLs (form submissions/success pages):
            # 'application_submit',
            # 'apply_success',
            # 'subscribe_email',
            # 'email_subscribe_success',
            # 'connect_request',
            # 'connect_success',
            # 'test',  # Include only if this is a real content page
        ]

    def location(self, item):
        return reverse(item)

    # Method to set priority per URL
    def get_priority(self, item):
        priority_map = {
            "index": 1.0,
            "lessons": 0.99,
            "articles": 0.9,
            "about_me": 0.9,
            "reviews": 0.9,
            # Default will use the class's priority (0.8)
        }
        return priority_map.get(item, self.priority)


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Article.objects.filter(status="published")

    def lastmod(self, obj):
        return obj.updated_at  # Make sure your model has this field

    def location(self, obj):
        return reverse("article", kwargs={"slug": obj.slug})
