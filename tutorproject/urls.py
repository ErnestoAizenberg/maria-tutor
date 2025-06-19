from django.urls import include, path
from main.custom_admin import custom_admin_site
urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path("", include("main.urls")),
]
