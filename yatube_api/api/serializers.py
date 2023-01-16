from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from posts.models import Post, Group


CHOICES = Group.objects.all()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault()
    )
    group = serializers.ChoiceField(choices=CHOICES)

    class Meta:
        model = Post
        fields = (
            'text',
            'pub_date',
            'author',
            'image',
            'group'
        )
        read_only_fields = ('author', 'pub_date')
        optional_fields = ('image', 'group')


class GroupSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        validators=[UniqueValidator(queryset=Group.objects.all())],
        read_only=True
    )

    class Meta:
        model = Group
        fields = (
            'title',
            'slug',
            'description',
        )
        required_fields = ('title', )
