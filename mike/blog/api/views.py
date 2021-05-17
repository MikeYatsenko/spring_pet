from rest_framework import viewsets, generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from news.api.serializers import PostSerializer, CommentSerializer
from news.api.permissions import IsAuthorOrReadOnly
from news.models import Post, Comment


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    lookup_field = "slug"
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostVoteAPIView(APIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        kwargs_slug = self.kwargs.get("slug")
        post = get_object_or_404(Post, slug=kwargs_slug)
        user = request.user
        post.voters.add(user)
        post.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(post, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, slug):
        kwargs_slug = self.kwargs.get("slug")
        post = get_object_or_404(Post, slug=kwargs_slug)
        user = request.user
        post.voters.add(user)
        post.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(post, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request_user = self.request.user
        kwargs_slug = self.kwargs.get("slug")
        post = get_object_or_404(Post, slug=kwargs_slug)
        serializer.save(author=request_user, post=post)


class CommentRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]


class CommentListAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        kwargs_slug = self.kwargs.get("slug")
        return Comment.objects.filter(post__slug=kwargs_slug).order_by("-creation_date")


class CommentVoteAPIView(APIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        kwargs_slug = self.kwargs.get("slug")
        comment = get_object_or_404(Post, slug=kwargs_slug)
        user = request.user
        comment.voters.add(user)
        comment.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(comment, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        kwargs_slug = self.kwargs.get("slug")
        comment = get_object_or_404(Post, slug=kwargs_slug)
        user = request.user
        comment.voters.remove(user)
        comment.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(comment, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)