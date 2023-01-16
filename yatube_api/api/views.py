from rest_framework import viewsets, mixins
from rest_framework.exceptions import PermissionDenied

from posts.models import Post, Group, Comment

from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class ListRetrieveViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pass


class MainViewSet(viewsets.ModelViewSet):
    '''Вьюсет для ограничения доступа к контенту, принадлежащего его автору.'''
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super(MainViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super(MainViewSet, self).perform_destroy(instance)


class PostViewSet(MainViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(MainViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        return super().get_queryset().filter(
            post=post_pk
        )


class GroupViewSet(ListRetrieveViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
