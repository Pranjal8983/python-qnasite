from django.db import models

from accounts.models import User
from core.db import SoftDeleteWithBaseModel


class Question(SoftDeleteWithBaseModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="questions")

    class Meta:
        ordering = ["-created_at"]
