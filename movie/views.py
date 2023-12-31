
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from django.conf import settings
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, DestroyModelMixin
import os
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
import base64
from storages.backends.s3boto3 import S3Boto3StorageFile
from django.core.files.storage import default_storage


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser()]


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return CreateMovieSerializer
        return MovieSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [AllowAny()]
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        userId = request.user.id
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        userlikes = UserLikes.objects.filter(
            user_id=userId, like=True).values_list('movie_id', 'id')
        movies_id = set()
        likeid = dict()

        for (movieid, id) in userlikes:
            movies_id.add(movieid)
            likeid[str(movieid)] = id

        data = []
        for movie in serializer.data:
            m = {**movie}
            if m['id'] in movies_id:
                m['like'] = True
                m['likeId'] = likeid[str(m['id'])]
            else:
                m['like'] = False
            data.append(m)

        return Response(data)


class UserLikesViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserLikes.objects.filter(user_id=self.request.user.id)

    def get_serializer_context(self):
        if self.request.method in ["PUT", 'PATCH']:
            return {'userId': self.request.user.id, 'id': self.kwargs['pk']}
        return {'userId': self.request.user.id}

    def get_serializer_class(self):
        if self.request.method in ["PUT", 'PATCH']:
            return UpdateUserLikeSerializer
        return UserLikeSerializer


class ProfileViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return ProfileSerializer
        return CreateProfileSerializer

    def get_serializer_context(self):
        return {'userId': self.request.user.id}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except:
            return Response({'detail': 'profile already existed'}, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProfilePictureViewSet(RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'delete']

    lookup_value_regex = '[a-zA-Z0-9_-]+\.(?:png|jpg|jpeg|gif|svg)'

    def get_queryset(self):
        return Profile.objects.filter(user_id=self.request.user.id)

    def retrieve(self, request, *args, **kwargs):

        profile = get_object_or_404(
            self.get_queryset(), picture='store/images/'+self.kwargs['pk'])

        file = default_storage.open(profile.picture.name, 'rb')
        file_url = default_storage.url(profile.picture.name)
        binary_fc = file.read()
        base64_utf8_str = base64.b64encode(binary_fc).decode('utf-8')

        ext = self.kwargs['pk'].split('.')[-1]
        dataurl = f'data:image/{ext};base64,{base64_utf8_str}'

        return Response({'dataurl': dataurl, 'url': file_url})

    def destroy(self, request, *args, **kwargs):
        profile = get_object_or_404(
            self.get_queryset(), picture='store/images/'+self.kwargs['pk'])
        if profile.picture:
            profile.picture.delete(save=False)
            profile.picture = ""
        profile.save()
        return Response({'dataurl': ""})
