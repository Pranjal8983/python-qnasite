from django.urls import path

from qna.views import answer, question

urlpatterns = [
    path(
        "",
        question.QuestionListView.as_view(),
        name="home",
    ),
    path(
        "question/create",
        question.QuestionCreateView.as_view(),
        name="create_question",
    ),
    path(
        "question/<int:pk>",
        question.QuestionDetailView.as_view(),
        name="question_detail",
    ),
    path(
        "question/<int:pk>/update",
        question.QuestionUpdateView.as_view(),
        name="update_question",
    ),
    path(
        "question/<int:pk>/delete",
        question.QuestionDeleteView.as_view(),
        name="delete_question",
    ),
    path(
        "question/<int:pk>/answer",
        answer.AnswerCreateView.as_view(),
        name="create_answer",
    ),
    path(
        "answer/<int:pk>/update",
        answer.AnswerUpdateView.as_view(),
        name="update_answer",
    ),
    path(
        "answer/<int:pk>/delete",
        answer.AnswerDeleteView.as_view(),
        name="delete_answer",
    ),
    path(
        "answer/<int:pk>/like",
        answer.LikeAnswerView.as_view(),
        name="like_answer",
    ),
]
