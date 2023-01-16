from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from posts.models import Post, Group, Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True
    )
    post = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'post',
            'text',
            'created'
        )


class GroupSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        validators=[UniqueValidator(queryset=Group.objects.all())],
        read_only=True
    )

    class Meta:
        model = Group
        fields = (
            'id',
            'title',
            'slug',
            'description',
        )
        required_fields = ('title', )
        read_only_fields = ('title', 'slug', 'description')


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        model = Post
        fields = (
            'id',
            'text',
            'author',
            'image',
            'group',
            'pub_date',
        )
        read_only_fields = ('author', 'pub_date')
        optional_fields = ('image', 'group')
