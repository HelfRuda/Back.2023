from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Post, Category, Tag, Comments
from .form import CommentsForm, PostForm
from .serializers import PostSerializer, CategorySerializer, TagSerializer, CommentSerializer

class AllPostsAPI(generics.ListAPIView):
    serializer_class = PostSerializer

    @swagger_auto_schema(operation_description="Получение всех постов")
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddPostAPI(generics.CreateAPIView):
    serializer_class = PostSerializer

    @swagger_auto_schema(operation_description="Создание поста",
                         request_body=PostSerializer,
                         responses={201: PostSerializer()})
    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditPostAPI(generics.RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @swagger_auto_schema(operation_description="Изменение поста",
                         request_body=PostSerializer,
                         responses={200: PostSerializer()})
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PostSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeletePostAPI(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @swagger_auto_schema(operation_description="Удаление поста")
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddCommentsAPI(generics.CreateAPIView):
    serializer_class = CommentSerializer

    @swagger_auto_schema(operation_description="Создание комментария",
                         request_body=CommentSerializer,
                         responses={201: CommentSerializer()})
    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)