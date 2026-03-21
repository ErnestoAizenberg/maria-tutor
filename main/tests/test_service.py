from django.test import TestCase

from main.views import calculate_reading_time


class TestCalculateReadingTime(TestCase):
    def test_empty_string_returns_zero(self):
        """Should return 0 minutes for empty content."""
        self.assertEqual(calculate_reading_time(""), 0)

    def test_single_word_returns_one_minute(self):
        """Should return 1 minute for content with few words."""
        self.assertEqual(calculate_reading_time("Hello"), 1)

    def test_exactly_words_per_minute_returns_one_minute(self):
        """Should return 1 minute when word count equals words_per_minute."""
        # Create string with exactly 200 words
        content = "word " * 11
        self.assertEqual(calculate_reading_time(content, words_per_minute=11), 1)

    def test_rounds_up_when_word_count_exceeds_wpm(self):
        """Should round up to 2 minutes when exceeding wpm."""
        content = "word " * 12
        self.assertEqual(calculate_reading_time(content, words_per_minute=11), 2)

    def test_one_word_less_than_wpm_returns_one_minute(self):
        """Should round up to 1 minute when content is less than wpm."""
        content = "word " * 10
        self.assertEqual(calculate_reading_time(content, words_per_minute=11), 1)

    def test_multiple_minutes_exact_division(self):
        """Should return exact minutes when word count is multiple of wpm."""
        content = "word " * 22
        self.assertEqual(calculate_reading_time(content, words_per_minute=11), 2)

    def test_complex_content_handling(self):
        """Should correctly count words in complex text."""
        content = "This is a sentence. This is another sentence with punctuation!"
        # 12 words total
        self.assertEqual(calculate_reading_time(content, words_per_minute=12), 1)

    def test_newlines_and_multiple_spaces(self):
        """Should handle various whitespace correctly."""
        content = "Word1\n\nWord2   Word3\tWord4"
        # 4 words total
        self.assertEqual(calculate_reading_time(content, words_per_minute=4), 1)

    def test_unicode_characters(self):
        """Should handle Unicode text correctly."""
        content = "Hello 世界 Привет 你好"
        # 4 words total
        self.assertEqual(calculate_reading_time(content, words_per_minute=4), 1)

    def test_mixed_whitespace_and_empty_lines(self):
        """Should handle various whitespace combinations."""
        content = "   \n\n   Hello   World   \n\n   "
        # 2 words total
        self.assertEqual(calculate_reading_time(content, words_per_minute=2), 1)

    def test_only_punctuation(self):
        """Should handle strings with only punctuation."""
        self.assertEqual(calculate_reading_time("!@#$%^&*()", words_per_minute=1), 0)

    def test_zero_words_per_minute(self):
        """Should raise ValueError when words_per_minute is zero."""
        with self.assertRaises(ValueError):
            calculate_reading_time("Hello World", words_per_minute=0)

    def test_negative_words_per_minute(self):
        """Should handle invalid negative words_per_minute."""
        with self.assertRaises(ValueError):
            calculate_reading_time("Hello World", words_per_minute=-50)
