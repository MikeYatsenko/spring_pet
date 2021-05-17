
from  rest_framework import serializers
from ..models  import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    creation_date = serializers.SerializerMethodField()
    upvotes_count = serializers. SerializerMethodField()
    user_has_voted = serializers. SerializerMethodField()

    class Meta:
         model = Comment
         exclude = ["post", "comment_voters", "updated_at"]

    def get_creation_date (self,instance):
        return instance.creation_date.strftime("%d %B %Y")

    def get_upvotes_count(self,instance):
        return instance.comment_voters.count()

    def get_user_has_voted(self,instance):
        request = self.context.get("request")
        return instance.comment_voters.filter(pk=request.user.pk).exists()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    creation_date = serializers.SerializerMethodField()
    slug = serializers.SlugField(read_only=True)
    comments_count = serializers.SerializerMethodField()
    user_has_commented = serializers.SerializerMethodField()
    upvotes_count = serializers.SerializerMethodField()
    user_has_voted = serializers.SerializerMethodField()

    class Meta:
        model = Post
        exclude = ["updated_at", "voters"]

    def get_creation_date(self, instance):
        return instance.creation_date.strftime("%d %B %Y")

    def get_comments_count(self,instance):
        return instance.comments.count()

    def get_user_has_commented(self,instance):
        request = self.context.get("request")
        return instance.comments.filter(author=request.user).exists()

    def get_upvotes_count(self,instance):
        return instance.voters.count()

    def get_user_has_voted(self,instance):
        request = self.context.get("request")
        return instance.voters.filter(pk=request.user.pk).exists()