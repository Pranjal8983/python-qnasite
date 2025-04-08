from django.urls import path
from .views import (
    QuestionListView,
    QuestionDetailView,
    QuestionCreateView,
    QuestionUpdateView,
    QuestionDeleteView,
    AnswerCreateView,
    AnswerUpdateView,
    AnswerDeleteView,
    LikeAnswerView,
)

urlpatterns = [
    path("", QuestionListView.as_view(), name="home"),
    path("question/create", QuestionCreateView.as_view(), name="create_question"),
    path("question/<int:pk>", QuestionDetailView.as_view(), name="question_detail"),
    path(
        "question/<int:pk>/update", QuestionUpdateView.as_view(), name="update_question"
    ),
    path(
        "question/<int:pk>/delete", QuestionDeleteView.as_view(), name="delete_question"
    ),
    path(
        "question/<int:pk>/answer",
        AnswerCreateView.as_view(),
        name="create_answer",
    ),
    path("answer/<int:pk>/update", AnswerUpdateView.as_view(), name="update_answer"),
    path("answer/<int:pk>/delete", AnswerDeleteView.as_view(), name="delete_answer"),
    path("answer/<int:pk>/like", LikeAnswerView.as_view(), name="like_answer"),
]
