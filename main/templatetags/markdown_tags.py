import markdown
from django import template
from django.utils.safestring import mark_safe
from bs4 import BeautifulSoup

register = template.Library()

@register.filter(is_safe=True)  # Ключевой параметр!
def markdown_to_html(text):
    if not text:
        return ""

    # 1. Отключаем автоэкранирование для исходного текста
    text = mark_safe(text)

    # 2. Обработка Markdown
    md = markdown.Markdown(
        extensions=['extra', 'nl2br', 'sane_lists'],
        output_format='html5'
    )

    # 3. Парсинг HTML с сохранением структуры
    soup = BeautifulSoup(md.convert(text), 'html.parser')

    # 4. Двойная обработка Markdown внутри HTML-тегов
    for element in soup.find_all(text=True):
        if element.parent.name not in ['script', 'style']:
            html = md.reset().convert(element.string)
            element.replace_with(BeautifulSoup(html, 'html.parser'))

    # 5. Возвращаем как безопасный HTML
    result = str(soup)
    return mark_safe(result)
