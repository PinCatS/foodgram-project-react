from djoser.views import UserViewSet

from api.paginator import DynamicLimitPaginator


class CustomUserViewSet(UserViewSet):
    pagination_class = DynamicLimitPaginator
