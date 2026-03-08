import logging

from .models import Page, Teacher

logger = logging.getLogger(__name__)


def create_default_pages(teacher_slug):
    """
    Creates default pages for a teacher if they don't already exist.

    Args:
        teacher_slug (str): The slug of the teacher to create pages for

    Returns:
        dict: Information about the created pages

    Raises:
        ValueError: If teacher is not found
    """
    # Get teacher or raise error
    teacher = Teacher.objects.filter(slug=teacher_slug).first()
    if not teacher:
        raise ValueError(f"Teacher with slug '{teacher_slug}' not found")

    # Default pages configuration
    pages_config = {
        "contacts": {
            "name": "Контакты",
            "is_navbar_button": True,
            "show_in_navbar": True,
            "show_in_footer": True,
            "title": f"Контакты {teacher.name} - Связь, Telegram-каналы и сотрудничество",
            "meta_description": f"Как связаться с {teacher.name}. {teacher.status}",
            "hero_title": f"Свяжитесь с {teacher.name}",
            "hero_sub_title": "Выберите удобный способ связи",
        },
        "lessons": {
            "name": "Уроки",
            "show_in_navbar": True,
            "show_in_footer": False,
            "title": f"Стоимость и форматы занятий • {teacher.name} | {teacher.status}",
            "meta_description": f"Расписание и описание уроков с {teacher.name}",
            "hero_title": f"Уроки с {teacher.name}",
            "hero_sub_title": "Расписание и описание занятий",
        },
        "about_me": {
            "name": "Обо мне",
            "show_in_navbar": True,
            "show_in_footer": True,
            "title": f"Обо мне | {teacher.name} - {teacher.status}",
            "meta_description": f"Подробная информация о {teacher.name}. {teacher.status}",
            "hero_title": teacher.name,
            "hero_sub_title": getattr(teacher, "description", ""),
            "og_type": "profile",
            "og_title": f"Обо мне - {teacher.name} | {teacher.status}",
        },
        "reviews": {
            "name": "Отзывы",
            "show_in_navbar": True,
            "show_in_footer": False,
            "title": f"🔬 {teacher.name} | Отзывы учеников о преподавателе",
            "meta_description": f"Отзывы учеников о занятиях с {teacher.name}",
            "hero_title": f"Отзывы о {teacher.name}",
            "hero_sub_title": f"Средний рейтинг: {teacher.aggregate_rating}/5",
            "og_title": f"{teacher.name} | Отзывы учеников о преподавателе",
            "og_site_name": f"{teacher.status} | {teacher.name}",
        },
        "articles": {
            "name": "Статьи",
            "show_in_navbar": False,
            "show_in_footer": True,
            "title": f"Статьи {teacher.name} | {teacher.status}",
            "meta_description": f"Полезные статьи и материалы от {teacher.name}",
            "hero_title": f"Статьи от {teacher.name}",
            "hero_sub_title": "Полезные материалы и советы",
        },
    }

    created_pages = []

    for slug, config in pages_config.items():
        # Check if page already exists
        if not Page.objects.filter(teacher=teacher, slug=slug).exists():
            # Generate common SEO fields
            seo_fields = {
                "og_title": config.get("og_title", config.get("title", "")),
                "og_description": config.get("meta_description", ""),
                "og_url": f"/{teacher.slug}/{slug}",
                "twitter_title": config.get("title", ""),
                "twitter_description": config.get("meta_description", ""),
            }

            try:
                # Create the page
                page = Page(
                    teacher=teacher,
                    slug=slug,
                    is_published=True,
                    **config,
                    **seo_fields,
                )
                page.save()
                created_pages.append(page)
            except Exception as e:
                # Log error and continue with other pages
                logger.error(
                    f"Error creating page {slug} for teacher {teacher.name}: {str(e)}"
                )

    return {
        "teacher": teacher.name,
        "created_pages": [p.name for p in created_pages],
        "total_created": len(created_pages),
    }
