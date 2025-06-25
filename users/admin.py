from django.contrib import admin
from users.models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'full_name', 'phone_number', 'language', 'created_at')
    search_fields = ('full_name', 'phone_number', 'telegram_id')
