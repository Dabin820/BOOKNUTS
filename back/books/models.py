# books/models.py
from django.db import models
from django.conf import settings
import datetime


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# 추후 조정
class Book(models.Model):
    isbn = models.CharField(max_length=20, primary_key=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='books'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    cover = models.URLField()  
    publisher = models.CharField(max_length=100)
    pub_date = models.DateField()
    author = models.CharField(max_length=100)
    author_info = models.TextField()
    author_photo = models.URLField()  
    customer_review_rank = models.FloatField()
    subTitle = models.CharField(max_length=100)
    itemPage = models.IntegerField() # 페이지 수

    def __str__(self):
        return self.title


class Thread(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    reading_date = models.DateField(default=datetime.date.today)
    cover_img = models.ImageField(upload_to="thread_cover_img/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_threads", blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class UserCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'category')


class UserLibrary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='library')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    saved_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')