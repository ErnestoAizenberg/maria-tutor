import logging

from .models import Teacher

logger = logging.getLogger("__name__")


def teacher_context(request):
    lang = request.GET.get("lang") or "ru"
    teacher = Teacher.objects.filter(is_active=True, lang=lang).first()
    if not teacher:
        logger.warning(f"No active teacher retrieved for language {lang}")

    return {
        "teacher": teacher,
    }
