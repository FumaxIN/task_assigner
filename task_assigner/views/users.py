from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework import permissions

from utils.views.mixins import PartialUpdateModelMixin
from utils.views.base import BaseModelViewSetPlain

from task_assigner.models import User
from task_assigner.serializers.users import UserSerializer



class UserViewSet(
    BaseModelViewSetPlain,
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    PartialUpdateModelMixin
):
    """
    API endpoint that allows users to be created, retrieved, updated, and deleted.
    """
    queryset = User.objects.all()
    lookup_field = 'external_id'
    permission_classes = (permissions.AllowAny,)
    # permission_action_classes = {
    #     'create': (permissions.IsAdminUser,),
    #     'list': (permissions.AllowAny,),
    #     'retrieve': (permissions.IsAuthenticated,),
    #     'partial_update': (permissions.IsAuthenticated,),
    #     'destroy': (permissions.IsAuthenticated,)
    # }

    serializer_class = UserSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned users to a given user.
        """
        queryset = self.queryset
        external_id = self.request.query_params.get('external_id', None)
        if external_id is not None:
            queryset = queryset.filter(external_id=external_id)
        return queryset