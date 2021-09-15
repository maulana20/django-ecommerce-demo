from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.forms import CustomUserCreationForm, CustomUserChangeForm
from account.models import UserBase, Shop

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = UserBase
    list_display = ('user_name', 'email', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'full_name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_name', 'email', 'full_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(UserBase, CustomUserAdmin)

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'created']
    search_fields = ['title']
