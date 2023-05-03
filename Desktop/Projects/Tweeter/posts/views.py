from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework import views
from rest_framework.decorators import action
from rest_framework import permissions

from .models import Tweet, TweetLike, TweetImage, Comment, CommentLike
from .serializers import TweetSerializer, TweetLikeSerializer, TweetImageSerializer, CommentSerializer, \
    CommentLikeSerializer, CommentDislikeSerializer
from .permissions import IsAuthorOrAllowAny


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    authentication_classes = [SessionAuthentication, ]
    permission_classes = [IsAuthorOrAllowAny, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['POST', ], detail=True, permission_classes=[permissions.IsAuthenticated])
    def like_tweet(self, request, pk=None):
        serializer = TweetLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                user=request.user,
                tweet_id=pk
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

# class TweetLikeDislikeAPIView(views.APIView):
#     def post(self, request, pk, *args, **kwargs):
#         serializer = TweetLikeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(
#                 user=request.user,
#                 tweet_id=pk
#             )
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)


class TweetImageViewSet(viewsets.ModelViewSet):
    queryset = TweetImage.objects.all()
    serializer_class = TweetImageSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, ]
    permission_classes = [IsAuthorOrAllowAny, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['POST', ], detail=True, permission_classes=[permissions.IsAuthenticated])
    def like_comment(self, request, pk=None):
        serializer = CommentLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                user=request.user,
                comment_id=pk
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @action(methods=['POST', ], detail=True, permission_classes=[permissions.IsAuthenticated])
    def dislike_comment(self, request, pk=None):
        serializer = CommentDislikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                user=request.user,
                comment_id=pk
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
