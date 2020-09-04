from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    # each of this ones is a section
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_("Personal info"), {"fields": ("name",)}),
        (
            _("Permissions"), {
                "fields": ("is_active", "is_staff", "is_superuser")}
        ),
        (_("Important dates"), {"fields": ("last_login", "logout")})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),  # classes to the page
            'fields': ('email', 'password1', 'password2'),
        }),
    )


# Overwrites the admin model from django
admin.site.register(models.User, UserAdmin)
