from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Subscribe, User
from .serializers import CustomUserSerializer, SubscribeSerializer
from api.paginator import DynamicLimitPaginator
from recipes.serializers import SimpleRecipeSerializer


class CustomUserViewSet(UserViewSet):
    pagination_class = DynamicLimitPaginator
    serializer_class = CustomUserSerializer

    @action(
        detail=False,
        url_path='subscriptions',
        serializer_class=SubscribeSerializer,
    )
    def subscriptions(self, request):
        user = request.user
        authors = user.subscribers.all()
        authors = [author.author for author in authors]
        page = self.paginate_queryset(authors)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(authors, many=True)
        return Response(serializer.data)

    @action(
        detail=True, methods=['post'], serializer_class=SimpleRecipeSerializer
    )
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, pk=id)[0]
        Subscribe.objects.create(
            author=author,
            user=request.user,
        )
        serializer = self.get_serializer(author)
        return Response(serializer.data)

    @subscribe.mapping.delete
    def unsubscribe(self, request, id=None):
        Subscribe.objects.filter(author=id, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
