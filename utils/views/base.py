from rest_framework.viewsets import GenericViewSet

from .mixins import GetPermissionClassesMixin, GetSerializerClassMixin


class BaseModelViewSetPlain(
    GetPermissionClassesMixin,
    GetSerializerClassMixin,
    GenericViewSet,
):
    pass