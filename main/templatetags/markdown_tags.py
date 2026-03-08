import markdown
from bs4 import BeautifulSoup
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(is_safe=True)
def markdown_to_html(text: str) -> str:
    """Convert makdown to safe HTML"""
    if not text:
        return ""

    text = mark_safe(text)
    md = markdown.Markdown(
        extensions=["extra", "nl2br", "sane_lists"], output_format="html"
    )
    soup = BeautifulSoup(md.convert(text), "html.parser")

    for element in soup.find_all(string=True):
        if element.parent and element.parent.name not in ["script", "style"]:
            html = md.reset().convert(element.string)
            element.replace_with(BeautifulSoup(html, "html.parser"))

    result = str(soup)
    return mark_safe(result)
