from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.views import serve
from django.urls import include, path
from django.views.decorators.cache import never_cache
from django.views.generic.base import TemplateView

from main.custom_admin import custom_admin_site

urlpatterns = [
    path("admin/", custom_admin_site.urls),
    path("", include("main.urls")),
    path("", include("telegram_bot.urls")),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
]

urlpatterns += static(
    settings.STATIC_URL, view=never_cache(serve), document_root=settings.STATIC_ROOT
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
