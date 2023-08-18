from typing import Iterable, Optional
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.core.files.storage import default_storage
# Create your models here.

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    dailyRentalRate = models.DecimalField(max_digits=6, decimal_places=1)
    numberInStock = models.PositiveIntegerField()
    create_at = models.DateField(auto_now=False, auto_now_add=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


class UserLikes(models.Model):
    like = models.BooleanField(blank=True, default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


class Profile(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(
        upload_to='store/images', blank=True, null=True)
    phone_number = models.CharField(max_length=255, validators=[
                                    MinLengthValidator(10), MaxLengthValidator(12)], null=True, blank=True)

    def __str__(self) -> str:
        return '{} {}'.format(self.first_name, self.last_name)

    def picture_tag(self):
        if self.picture.name != '':
            return format_html('<img  src="{}"  class="profile"/>'.format(self.picture.url))
        else:
            return ""

    def save(self, *args, **kwargs) -> None:

        if not self.pk:
            obj = Profile.objects.get(pk=self.pk)
            print(obj.picture)
            print(self.picture)
            if self.picture and obj.picture and obj.picture.name != ('store/images/'+self.picture.name):
                obj.picture.delete(save=False)
        return super(Profile, self).save(*args, **kwargs)
