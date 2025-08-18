from rest_framework.serializers import ModelSerializer
from communitty.models import Discussion, Comment, Tag, DiscussionCategory


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class DiscussionCategorySerializer(ModelSerializer):
    class Meta:
        model = DiscussionCategory
        fields = '__all__'


class DiscussionSerializer(ModelSerializer):
    class Meta:
        model = Discussion
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'