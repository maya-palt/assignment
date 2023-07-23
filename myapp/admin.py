from django.contrib import admin

# Register your models here.
from .models import *
from rest_framework.authtoken.models import Token

# Register the Token model with the admin site
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('get_token',)

    def get_token(self, obj):
        try:
            return Token.objects.get(user=obj).key
        except Token.DoesNotExist:
            return "N/A"

    get_token.short_description = 'Token'

# Unregister the default User admin
admin.site.unregister(User)

# Register User with the custom admin class
admin.site.register(User, CustomUserAdmin)


admin.site.register(Certificate)
admin.site.register(CertificateFile)
admin.site.register(VerificationID)
VerificationID