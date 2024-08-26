from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("services/", include("services.urls", namespace="services")),
    path("user/", include("users.urls", namespace="user")),
    path("", include("blog.urls", namespace="blog")),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)  # Добавление маршрута для обслуживания медиафайлов
