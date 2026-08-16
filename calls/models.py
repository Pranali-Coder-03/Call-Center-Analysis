from django.db import models


class CallRecording(models.Model):

    STATUS_CHOICES = [
        ("uploaded", "Uploaded"),
        ("analyzing", "Analyzing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    file_name = models.CharField(
        max_length=255
    )

    file_url = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="uploaded"
    )

    storage_path = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    summary = models.TextField(
        blank=True
    )

    sentiment = models.CharField(
        max_length=100,
        blank=True
    )

    customer_issue = models.TextField(
        blank=True
    )

    resolution = models.TextField(
        blank=True
    )

    agent_performance = models.TextField(
        blank=True
    )

    key_topics = models.TextField(
        blank=True
    )

    action_items = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    analyzed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.file_name