from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic.base import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]

# API URLS
api_urlpatterns = [
    # API base url
    path("v1/", include("task_assigner.api_router")),
    path("v1/schema", SpectacularAPIView.as_view(), name="schema"),
]

if settings.DEBUG:
    api_urlpatterns += [
        path(
            "v1/schema/swagger/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path(
            "v1/schema/redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="redoc",
        ),
        path("", RedirectView.as_view(url="/v1/schema/swagger/", permanent=False)),
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]

urlpatterns += api_urlpatterns
