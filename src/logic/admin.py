from django.contrib import admin
from logic.models import User, Subscription

admin.site.register(User)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    fields = ['subscriber', 'birthday_person', 'notification_time']