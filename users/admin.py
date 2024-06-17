from django.contrib import admin
from .models import CustomUser, UserData

from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    list_display = ( 'username', 'email', 'pk', 'date_joined', 'last_login', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserDataAdmin(admin.ModelAdmin):
    list_display = ('user','pk', 'amount')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserData, UserDataAdmin)