from django.db import models

from accounts.models import User
from core.db import SoftDeleteWithBaseModel
from qna.models.question import Question


class Answer(SoftDeleteWithBaseModel):
    content = models.TextField()
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers")
    likes = models.ManyToManyField(User, related_name="liked_answers", blank=True)

    class Meta:
        ordering = ["created_at"]
