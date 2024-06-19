from django.contrib import admin
from logic.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
