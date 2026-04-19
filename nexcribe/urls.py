from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

admin.site.site_header = "Nexcribe Admin"
admin.site.site_title = "Nexcribe"
admin.site.index_title = "Content Management"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ckeditor/", include("ckeditor_uploader.urls")),

    path("api/v1/auth/token/", TokenObtainPairView.as_view(), name="token-obtain"),
    path("api/v1/auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("api/v1/auth/", include("accounts.urls")),

    path("api/v1/platforms/", include("platforms.urls")),
    path("api/v1/reviews/", include("reviews.urls")),
    path("api/v1/blog/", include("blog.urls")),
    path("api/v1/submissions/", include("submissions.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)