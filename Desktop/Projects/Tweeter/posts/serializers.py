from rest_framework import serializers
from django.db.utils import IntegrityError

from .models import Tweet, TweetLike, TweetImage, Comment, CommentLike, CommentDislike


class TweetSerializer(serializers.ModelSerializer):
    likes_dislikes = serializers.ReadOnlyField(source='get_likes_dislikes')

    class Meta:
        model = Tweet
        fields = "__all__"
        read_only_fields = ['user', ]


class TweetLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetLike
        fields = "__all__"
        read_only_fields = ['user', 'tweet', ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            tweet_like = TweetLike.objects.get(
                user=validated_data['user'],
                tweet_id=validated_data['tweet_id']
            )
            if tweet_like.is_like != validated_data['is_like']:
                tweet_like.is_like = not tweet_like.is_like
                tweet_like.save()
            return tweet_like


class TweetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetImage
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user', ]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs['user'] = self.context['request'].user
        return attrs


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = "__all__"
        read_only_fields = ['user', 'comment', ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            comm_like = CommentLike.objects.get(
                user=validated_data['user'],
                comment_id=validated_data['comment_id']
            )
            if comm_like.mark != validated_data['mark']:
                comm_like.mark = not comm_like.mark
                comm_like.save()
            return comm_like


class CommentDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentDislike
        fields = "__all__"
        read_only_fields = ['user', 'comment', ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            comm_like = CommentDislike.objects.get(
                user=validated_data['user'],
                comment_id=validated_data['comment_id']
            )
            if comm_like.mark != validated_data['mark']:
                comm_like.mark = not comm_like.mark
                comm_like.save()
            return comm_like
