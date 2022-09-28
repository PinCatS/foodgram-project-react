from rest_framework.pagination import PageNumberPagination


class DynamicLimitPaginator(PageNumberPagination):
    page_size_query_param = 'limit'
