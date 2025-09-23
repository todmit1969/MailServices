from django.contrib import admin
from .models import SendAttempt


@admin.register(SendAttempt)
class SendAttemptAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'status', 'attempt_datetime', 'server_response')
    list_filter = ('status', 'attempt_datetime', 'mailing')