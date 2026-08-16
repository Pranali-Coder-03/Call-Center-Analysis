from django.contrib import admin
from .models import CallRecording


@admin.register(CallRecording)
class CallRecordingAdmin(admin.ModelAdmin):

    list_display = (
        "file_name",
        "status",
        "sentiment",
        "created_at",
    )

    list_filter = (
        "status",
        "sentiment",
        "created_at",
    )

    search_fields = (
        "file_name",
        "summary",
    )