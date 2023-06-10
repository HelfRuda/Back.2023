from rest_framework import serializers
from .models import Post, Category, Tag, Comments

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'picture')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('id', 'text_comment', 'post')

class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'picture', 'author', 'date', 'category', 'tags', 'comments')

    def create(self, validated_data):
        category_data = self.validated_data.pop('category')
        tags_data = self.validated_data.pop('tags')
        post = Post.objects.create(**self.validated_data)
        category = Category.objects.create(**category_data)
        post.category = category
        for tag_data in tags_data:
            tag = Tag.objects.create(**tag_data)
            post.tags.add(tag)
        post.save()
        return post
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.author = validated_data.get('author', instance.author)
        instance.date = validated_data.get('date', instance.date)

        category_data = validated_data.get('category')
        if category_data:
            category = instance.category
            category.name = category_data.get('name', category.name)
            category.save()

        tags_data = validated_data.get('tags')
        if tags_data:
            instance.tags.clear()
            for tag_data in tags_data:
                tag, _ = Tag.objects.get_or_create(name=tag_data['name'])
                instance.tags.add(tag)

        instance.save()
        return instance