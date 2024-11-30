from django.contrib import admin
from .models import CustomUser, UserData

from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'pk',
                    'date_joined', 'phone_verified', 'email_verified', 'last_login',)
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login')
    list_filter = ('phone_verified', 'email_verified')
    date_hierarchy = 'date_joined'
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)


class UserDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'referral_count')
    ordering = ('amount', 'referral_count')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserData, UserDataAdmin)
