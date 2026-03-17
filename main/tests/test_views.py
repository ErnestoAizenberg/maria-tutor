from django.test import Client, TestCase
from django.urls import reverse

from main.models import Article
import main.views as views


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
        response = self.client.get(reverse(views.index))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/index-purple.html")
        self.assertContains(response, "Test Article")
        self.assertNotContains(response, "Unpublished Article")

    # Test article detail view
    def test_article_view(self):
        response = self.client.get(reverse(views.article, args=["test-article"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/article-purple.html")
        self.assertContains(response, "This is a test article content")
        self.assertContains(response, "мин чтения")

    def test_article_view_404(self):
        response = self.client.get(
            reverse(views.article, args=["non-existent-article"])
        )
        self.assertEqual(response.status_code, 404)

    # Test articles list view
    def test_articles_view(self):
        response = self.client.get(reverse(views.articles))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/articles.html")
        self.assertEqual(
            len(response.context["articles"]), 1
        )  # Only published articles

    # Test application submission
    def test_application_submit_valid(self):
        response = self.client.post(
            reverse(views.application_submit),
            {
                "name": "Test User",
                "email": "test@example.com",
                "subject": "biology",
                "goal": "Learn basics",
            },
        )
        self.assertRedirects(response, reverse(views.apply_success))

    def test_application_submit_invalid(self):
        response = self.client.post(
            reverse(views.application_submit), {"name": "", "email": "test@example.com"}
        )
        self.assertEqual(response.status_code, 302)  # Should redirect back

    # Test contact form
    def test_connect_request_valid(self):
        response = self.client.post(
            reverse(views.connect_request),
            {
                "name": "Test User",
                "email": "test@example.com",
                "message": "Test message",
            },
        )
        self.assertRedirects(response, reverse(views.connect_success))

    def test_connect_request_invalid(self):
        response = self.client.post(
            reverse(views.connect_request),
            {"name": "Test User", "email": "invalid-email", "message": ""},
        )
        self.assertEqual(response.status_code, 302)

    # Test email subscription
    def test_subscribe_email_valid(self):
        response = self.client.post(
            reverse(views.subscribe_email), {"email": "test@example.com"}
        )
        self.assertRedirects(response, reverse(views.email_subscribe_success))

    def test_subscribe_email_invalid(self):
        response = self.client.post(
            reverse(views.subscribe_email), {"email": "not-an-email"}
        )
        self.assertEqual(response.status_code, 302)

    # Test success pages
    def test_success_pages(self):
        response = self.client.get(reverse(views.apply_success))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse(views.connect_success))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse(views.email_subscribe_success))
        self.assertEqual(response.status_code, 200)

    def test_robots_txt(self):
        response = self.client.get(reverse(views.robots_txt))
        self.assertEqual(response.status_code, 200)

    def test_policy(self):
        response = self.client.get(reverse(views.policy))
        self.assertEqual(response.status_code, 200)

    def test_search_view(self):
        response = self.client.get(reverse(views.search_view))
        self.assertEqual(response.status_code, 200)

    def test_lessons(self):
        response = self.client.get(reverse(views.lessons))
        self.assertEqual(response.status_code, 200)

    def test_about_me(self):
        response = self.client.get(reverse(views.about_me))
        self.assertEqual(response.status_code, 200)

    def test_science(self):
        response = self.client.get(reverse(views.science))
        self.assertEqual(response.status_code, 200)

    def test_articles_by_tag(self):
        response = self.client.get(
            reverse(views.articles_by_tag, kwargs={"slug": "non-existent-tag-slug"})
        )
        self.assertEqual(response.status_code, 404)

    def test_articles(self):
        response = self.client.get(reverse(views.articles))
        self.assertEqual(response.status_code, 200)

    def test_test(self):
        response = self.client.get(reverse(views.test))
        self.assertEqual(response.status_code, 200)

    def test_contacts(self):
        response = self.client.get(reverse(views.contacts))
        self.assertEqual(response.status_code, 200)

    def test_reviews(self):
        response = self.client.get(reverse(views.reviews))
        self.assertEqual(response.status_code, 200)

    def test_async_program(self):
        response = self.client.get(reverse(views.async_program))
        self.assertEqual(response.status_code, 200)

    def test_bio_in_english(self):
        response = self.client.get(reverse(views.bio_in_english))
        self.assertEqual(response.status_code, 200)

    def test_group_programs(self):
        response = self.client.get(reverse(views.group_programs))
        self.assertEqual(response.status_code, 200)

    def test_olympiad_prep(self):
        response = self.client.get(reverse(views.olympiad_prep))
        self.assertEqual(response.status_code, 200)

    def test_one_on_one(self):
        response = self.client.get(reverse(views.one_on_one))
        self.assertEqual(response.status_code, 200)

    def test_subsidized(self):
        response = self.client.get(reverse(views.subsidized))
        self.assertEqual(response.status_code, 200)

    def test_lesson_details(self):
        response = self.client.get(reverse(views.lesson_details))
        self.assertEqual(response.status_code, 200)

    def test_application(self):
        response = self.client.get(reverse(views.application))
        self.assertEqual(response.status_code, 200)

    def test_tutor_consultation(self):
        response = self.client.get(reverse(views.tutor_consultation))
        self.assertEqual(response.status_code, 200)
