from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import SimpleRouter

from .views import ReadOnlyTagViewSet

app_name = 'api'

router_v1 = SimpleRouter()

router_v1.register('tags', ReadOnlyTagViewSet, basename='tag')

urlpatterns = [
    path('', include(router_v1.urls), name='api'),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

schema_view = get_schema_view(
    openapi.Info(
        title='Foodgram API',
        default_version='v1',
        description='Документация для приложения api проекта Foodgram',
        contact=openapi.Contact(email='admin@foodgram.ru'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    re_path(
        r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    re_path(
        r'^redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc',
    ),
]
