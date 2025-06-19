from django.core import mail
from django.test import Client, TestCase
from django.urls import reverse

from main.models import Article


class ViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test data that will be used by all test methods
        cls.article = Article.objects.create(
            title="Test Article",
            slug="test-article",
            content="This is a test article content.",
            status="published",
        )
        cls.unpublished_article = Article.objects.create(
            title="Unpublished Article",
            slug="unpublished-article",
            content="This should not be visible.",
            status="draft",
        )

    def setUp(self):
        self.client = Client()

    # Test index view
    def test_index_view(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/index-purple.html")
        self.assertContains(response, "Test Article")
        self.assertNotContains(response, "Unpublished Article")

    # Test article detail view
    def test_article_view(self):
        response = self.client.get(reverse("article", args=["test-article"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/article-purple.html")
        self.assertContains(response, "This is a test article content")
        self.assertContains(response, "мин чтения")

    def test_article_view_404(self):
        response = self.client.get(reverse("article", args=["non-existent-article"]))
        self.assertEqual(response.status_code, 404)

    # Test articles list view
    def test_articles_view(self):
        response = self.client.get(reverse("articles"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/articles.html")
        self.assertEqual(
            len(response.context["articles"]), 1
        )  # Only published articles

    # Test application submission
    def test_application_submit_valid(self):
        response = self.client.post(
            reverse("application_submit"),
            {
                "name": "Test User",
                "email": "test@example.com",
                "subject": "Math",
                "goal": "Learn basics",
            },
        )
        self.assertRedirects(response, reverse("apply_success"))

    def test_application_submit_invalid(self):
        response = self.client.post(
            reverse("application_submit"), {"name": "", "email": "test@example.com"}
        )
        self.assertEqual(response.status_code, 302)  # Should redirect back

    # Test contact form
    def test_connect_request_valid(self):
        response = self.client.post(
            reverse("connect_request"),
            {
                "name": "Test User",
                "email": "test@example.com",
                "message": "Test message",
            },
        )
        self.assertRedirects(response, reverse("connect_success"))

    def test_connect_request_invalid(self):
        response = self.client.post(
            reverse("connect_request"),
            {"name": "Test User", "email": "invalid-email", "message": ""},
        )
        self.assertEqual(response.status_code, 302)

    # Test email subscription
    def test_subscribe_email_valid(self):
        response = self.client.post(
            reverse("subscribe_email"), {"email": "test@example.com"}
        )
        self.assertRedirects(response, reverse("email_subscribe_success"))

    def test_subscribe_email_invalid(self):
        response = self.client.post(
            reverse("subscribe_email"), {"email": "not-an-email"}
        )
        self.assertEqual(response.status_code, 302)

    # Test success pages
    def test_success_pages(self):
        response = self.client.get(reverse("apply_success"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("connect_success"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("email_subscribe_success"))
        self.assertEqual(response.status_code, 200)
