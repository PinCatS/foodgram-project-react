from djoser.conf import settings
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from common.paginators import DynamicLimitPaginator
from common.utils import follow, unfollow
from users.models import Subscribe, User
from users.serializers import CustomUserSerializer, SubscribeSerializer


class CustomUserViewSet(UserViewSet):
    pagination_class = DynamicLimitPaginator
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = settings.PERMISSIONS.current_user
        if self.action == 'subscriptions':
            self.permission_classes = settings.PERMISSIONS.subscriptions
        if self.action == 'subscribe':
            self.permission_classes = settings.PERMISSIONS.subscribe

        return super().get_permissions()

    @action(
        detail=False,
        url_path='subscriptions',
        serializer_class=SubscribeSerializer,
    )
    def subscriptions(self, request):
        user = request.user
        subscriptions = user.subscriptions.all()
        authors = [subscription.author for subscription in subscriptions]
        page = self.paginate_queryset(authors)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(authors, many=True)
        return Response(serializer.data)

    @action(
        detail=True, methods=['post'], serializer_class=SubscribeSerializer
    )
    def subscribe(self, request, id=None):  # noqa: A002
        return follow(self, request, id, User, 'author', Subscribe)

    @subscribe.mapping.delete
    def unsubscribe(self, request, id=None):  # noqa: A002
        return unfollow(request, id, 'author', Subscribe)
