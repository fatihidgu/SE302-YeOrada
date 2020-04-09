from django.contrib import admin

# Register your models here.
from YeOradaApp.models import *
from django.contrib.auth.admin import UserAdmin

from .forms import RegisteredUserCreationForm, RegisteredUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = RegisteredUserCreationForm
    form = RegisteredUserChangeForm
    model = RegisteredUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'name', 'surname', 'password', 'isCustomer', 'isClient', 'isAdmin',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'username', 'name', 'surname', 'is_staff', 'is_active', 'isCustomer', 'isClient', 'isAdmin',)}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(RegisteredUser, CustomUserAdmin)
admin.site.register(Customer)
admin.site.register(Client)
admin.site.register(Admin)
admin.site.register(Comment)
admin.site.register(CommentAnswer)
admin.site.register(CommentLike)
admin.site.register(ClientCuisine)

