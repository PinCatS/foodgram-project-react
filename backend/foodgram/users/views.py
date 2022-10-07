from django.shortcuts import get_object_or_404
from djoser.conf import settings
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Subscribe, User
from .serializers import CustomUserSerializer, SubscribeSerializer
from api.paginator import DynamicLimitPaginator


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
        subscriptions = user.subscribers.all()
        authors = [subscription.author for subscription in subscriptions]
        page = self.paginate_queryset(authors)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(authors, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], serializer_class=None)
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, pk=id)
        Subscribe.objects.create(
            author=author,
            user=request.user,
        )
        serializer = SubscribeSerializer(author)
        return Response(serializer.data)

    @subscribe.mapping.delete
    def unsubscribe(self, request, id=None):
        subscription = get_object_or_404(
            Subscribe, author__id=id, user=request.user
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
