from rest_framework import viewsets, mixins
from rest_framework.exceptions import PermissionDenied

from posts.models import Post, Group

from .serializers import PostSerializer, GroupSerializer


class ListRetrieveViewSet(
    mixins.ListAPIView,
    mixins.RetrieveAPIView,
    viewsets.GenericViewSet
):
    pass


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super(PostViewSet, self).perform_destroy(instance)


class GroupViewSet(
    ListRetrieveViewSet
):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
