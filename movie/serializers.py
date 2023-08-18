from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        print("hi fjkfjdkljfkdsjkfjdkjfkdjfkdjkfjdkjfjkdjfkfjkfjkdsjfkj")
        token['username'] = user.username
        token['isAdmin'] = user.is_staff
        return token


class GenreSerializer(ModelSerializer):

    class Meta:
        model = Genre
        fields = ['id', 'name']


class MovieSerializer(ModelSerializer):
    genre = GenreSerializer()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'genre',
                  'numberInStock', 'dailyRentalRate',]


class CreateMovieSerializer(ModelSerializer):

    class Meta:

        model = Movie
        fields = ['title', 'genre', 'numberInStock', 'dailyRentalRate',]


class UserLikeSerializer(ModelSerializer):
    movie_title = serializers.SerializerMethodField(
        method_name='getMovie', read_only=True)

    class Meta:
        model = UserLikes
        fields = ['id', 'like', 'movie_title', 'movie']

    def getMovie(self, instance: UserLikes):
        return instance.movie.title

    def create(self, validated_data):
        data = {**validated_data, 'user_id': self.context['userId']}
        return super().create(data)


class UpdateUserLikeSerializer(ModelSerializer):
    class Meta:
        model = UserLikes
        fields = ['like']

    def update(self, instance, validated_data):
        data = {**validated_data,
                'user_id': self.context['userId']}
        return super().update(instance, data)


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['user']


class CreateProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name',
                  'date_of_birth', 'phone_number', 'picture']

    def create(self, validated_data):
        data = {**validated_data, 'user_id': self.context['userId']}
        return super().create(data)

    def update(self, instance, validated_data):
        data = {**validated_data, 'user_id': self.context['userId']}
        return super().update(instance, data)


class ProfilePictureSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ['picture']
