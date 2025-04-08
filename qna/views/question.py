from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from qna.forms import AnswerForm, QuestionForm
from qna.models import Question


class QuestionListView(ListView):
    """
    View for listing questions
    """

    model = Question
    template_name = "qna/home.html"
    context_object_name = "questions"
    ordering = ["-created_at"]
    paginate_by = 10


class QuestionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    View for creating questions
    """

    model = Question
    form_class = QuestionForm
    template_name = "qna/create_question.html"
    success_url = reverse_lazy("home")
    success_message = "Your question has been posted!"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("question_detail", kwargs={"pk": self.object.pk})


class QuestionDetailView(DetailView):
    """
    View for displaying a single question
    """

    model = Question
    template_name = "qna/question_detail.html"
    context_object_name = "question"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["answers"] = self.object.answers.all()
        if self.request.user.is_authenticated:
            context["form"] = AnswerForm()
        return context


class QuestionUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    View for updating questions
    """

    model = Question
    form_class = QuestionForm
    template_name = "qna/update_question.html"
    success_message = "Your question has been updated!"

    def get_queryset(self):
        return Question.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy("question_detail", kwargs={"pk": self.object.pk})


class QuestionDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    View for deleting questions
    """

    model = Question
    template_name = "qna/delete_question.html"
    success_url = reverse_lazy("home")
    success_message = "Your question has been deleted!"

    def get_queryset(self):
        return Question.objects.filter(author=self.request.user)
