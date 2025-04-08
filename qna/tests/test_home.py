from django.urls import reverse

from core.base_test import BaseTestCase
from qna.models import Question


class HomePageTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.create_user()
        self.questions = []
        # Create 15 questions to test pagination
        for i in range(15):
            self.questions.append(
                Question.objects.create(
                    title=f"Test Question {i}",
                    content=self.faker.paragraph(),
                    author=self.user,
                )
            )

    def test_template(self):
        """
        To make sure that the correct template is used
        """
        response = self.make_get_request(reverse("home"))
        self.assertTemplateUsed(response, "qna/home.html")

    def test_pagination(self):
        """
        To make sure that pagination works correctly
        """
        response = self.make_get_request(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["questions"]), 10
        )  # 10 questions per page

        # Test second page
        response = self.make_get_request(reverse("home") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["questions"]), 5)  # Remaining 5 questions

    def test_question_ordering(self):
        """
        To make sure that questions are ordered by created_at in descending order
        """
        response = self.make_get_request(reverse("home"))
        questions = response.context["questions"]
        self.assertTrue(
            all(
                questions[i].created_at >= questions[i + 1].created_at
                for i in range(len(questions) - 1)
            )
        )

    def test_authenticated_user_sees_ask_button(self):
        """
        To make sure that authenticated users see the 'Ask Question' button
        """
        self.authenticate(self.user)
        response = self.make_get_request(reverse("home"))
        self.assertContains(response, "Ask Question")

    def test_unauthenticated_user_no_ask_button(self):
        """
        To make sure that unauthenticated users don't see the 'Ask Question' button
        """
        response = self.make_get_request(reverse("home"))
        self.assertNotContains(response, "Ask Question")
