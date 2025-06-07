# books/serializers.py
from rest_framework import serializers
from .models import Category, Book, Thread, Comment, UserCategory, UserLibrary
from django.contrib.auth import get_user_model


User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Book
        fields = [
            'isbn', 'title', 'description', 'cover', 'publisher', 'pub_date',
            'author', 'author_info', 'author_photo', 'customer_review_rank',
            'subTitle', 'category', 'category_id', 'itemPage',
        ]

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'profile_img']


class ThreadSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    book = BookSerializer(read_only=True)
    # book_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Book.objects.all(), source='book', write_only=True
    # )
    like_count = serializers.IntegerField(source='likes.count', read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = [
            'id', 'book','user', 'title', 'content',
            'reading_date', 'cover_img', 'created_at', 'updated_at', 'like_count','is_liked'
        ]
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'profile_img')


class CommentSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    thread = ThreadSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'


class UserCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = UserCategory
        fields = ['id', 'user', 'category', 'category_id']


class UserLibrarySerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), source='book', write_only=True
    )

    class Meta:
        model = UserLibrary
        fields = ['id', 'user', 'book', 'book_id', 'saved_date']