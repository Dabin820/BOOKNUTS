# accounts/models.py
import uuid
import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from books.models import Category

def profile_img_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('user_profile_img', filename)

class User(AbstractUser):
    # 나이
    age = models.PositiveIntegerField(null=True)

    # 연간 독서량
    annual_reading_amount = models.PositiveIntegerField(blank=True, null=True)

    # 프로필 사진
    profile_img = models.ImageField(
        upload_to=profile_img_upload_to,
        blank=True,
        null=True,
    )

    # 관심 장르 (다중 선택, M:N 관계)
    interested_genres = models.ManyToManyField(
        Category,
        blank=True,
        related_name="users",
    )

    # 팔로잉
    followings = models.ManyToManyField(
        'self', symmetrical=False, related_name='followers'
    )

    def __str__(self):
        return self.username
