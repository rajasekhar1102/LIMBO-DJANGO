from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from django.utils.translation import gettext_lazy as _
from movie.models import Profile
# Register your models here.


class ProfileInline(admin.StackedInline):
    model = Profile
    fields = ['first_name', 'last_name',
              'date_of_birth', 'phone_number', 'picture']
    readonly_fields = ['picture_tag']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password",)}),
        (_("Personal info"), {"fields": ("email",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", 'email', "password1", "password2"),
            },
        ),
    )
    list_display = ("username", "email",  "is_staff")

    search_fields = ("username",  "email")
    inlines = [ProfileInline]
