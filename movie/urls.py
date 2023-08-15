from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('userlikes', UserLikesViewSet, basename='userlikes')
router.register('genres', GenreViewSet, basename='genre')
router.register('movies', MovieViewSet, basename='movie')
router.register('profile', ProfileViewSet, basename='profile')
router.register('media', ProfilePictureViewSet,
                basename='profilepic')
urlpatterns = router.urls
