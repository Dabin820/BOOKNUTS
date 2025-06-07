# accounts/serializers.py
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from books.models import Category


class CustomRegisterSerializer(RegisterSerializer):
    age = serializers.IntegerField(required=True)
    interested_genres_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='interested_genres',
        many=True,
        write_only=True,
        required=True
    )
    annual_reading_amount = serializers.IntegerField(required=False)
    profile_img = serializers.ImageField(required=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['age'] = self.validated_data.get('age', '')
        data['annual_reading_amount'] = self.validated_data.get('annual_reading_amount', None)
        data['profile_img'] = self.validated_data.get('profile_img', None)
        return data

    def custom_signup(self, request, user):
        user.age = self.validated_data.get('age')
        user.annual_reading_amount = self.validated_data.get('annual_reading_amount', None)
        user.profile_img = self.validated_data.get('profile_img', None)
        user.save()

        interested_genres = self.validated_data.get('interested_genres', [])
        user.interested_genres.set(interested_genres)



class UserSerializer(serializers.ModelSerializer):
    interested_genres = serializers.StringRelatedField(many=True, read_only=True)
    followers = serializers.StringRelatedField(many=True, read_only=True)
    followings = serializers.StringRelatedField(many=True, read_only=True)
    interested_genres_ids = serializers.SerializerMethodField(read_only=True)

    def get_interested_genres_ids(self, obj):
        return [c.id for c in obj.interested_genres.all()]

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'username',
            'email',
            'age',
            'annual_reading_amount',
            'profile_img',
            'interested_genres',
            'followers',
            'followings',
            'interested_genres_ids',  # read-only
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    interested_genres_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='interested_genres',
        many=True,
        required=False,
    )
    interested_genres = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'username',        # read-only
            'email',           # read-only
            'age',
            'annual_reading_amount',
            'profile_img',
            'interested_genres',        # read-only (이름 목록)
            'interested_genres_ids',    # read/write (id 배열)
        ]
        read_only_fields = ['username', 'email']    # 수정 제한할 경우 설정

