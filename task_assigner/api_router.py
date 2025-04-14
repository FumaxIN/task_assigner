from core import settings
from django.urls import path, include
from rest_framework_nested import routers

from task_assigner.views.auth import APIRegistrationView, APILoginView

app_name = "task_assigner"

router = routers.SimpleRouter(trailing_slash=False)
if settings.DEBUG:
    router = routers.DefaultRouter(trailing_slash=False)

# router.register()


auth_urls = [
    path("register", APIRegistrationView.as_view(), name="register"),
    path("login", APILoginView.as_view(), name="login"),
]

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include(auth_urls)),
]
