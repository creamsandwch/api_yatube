from django.urls import path, include

from rest_framework.routers import DefaultRouter

from rest_framework.authtoken.views import obtain_auth_token

from .views import PostViewSet, GroupViewSet


router = DefaultRouter()

router.register(r'posts', PostViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/api-token-auth/', obtain_auth_token),
]
