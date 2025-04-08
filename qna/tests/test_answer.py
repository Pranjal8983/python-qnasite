from django.urls import reverse

from core.base_test import BaseTestCase
from qna.models import Answer, Question


class AnswerCreateTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.create_user()
        self.other_user = self.create_user()
        self.question = Question.objects.create(
            title=self.faker.sentence(),
            content=self.faker.paragraph(),
            author=self.other_user,
        )
        self.authenticate(self.user)
        self.update_valid_input()

    def update_valid_input(self):
        """
        This function is responsible for updating the valid inputs and
        creating data in databases as required
        """
        self.persisted_valid_inputs = {
            "content": self.faker.paragraph(),
        }

    def test_template(self):
        """
        To make sure that the correct template is used
        """
        response = self.make_get_request(
            reverse("create_answer", args=[self.question.id])
        )
        self.assertTemplateUsed(response, "qna/question_detail.html")

    def test_success(self):
        """
        To make sure that the answer is created successfully
        """
        data = self.get_valid_inputs()
        response = self.make_post_request(
            reverse("create_answer", args=[self.question.id]), data
        )
        self.assertEqual(response.status_code, 302)
        self.assert_database_has(Answer, {"content": data["content"]})

    def test_cannot_answer_own_question(self):
        """
        To make sure that users cannot answer their own questions
        """
        own_question = Question.objects.create(
            title=self.faker.sentence(),
            content=self.faker.paragraph(),
            author=self.user,
        )
        data = self.get_valid_inputs()
        response = self.make_post_request(
            reverse("create_answer", args=[own_question.id]), data
        )
        self.assertEqual(response.status_code, 200)  # Returns with error
        self.assertFalse(Answer.objects.filter(content=data["content"]).exists())

    def test_failure(self):
        """
        To make sure that the answer is not created if the data is invalid
        """
        data = self.get_valid_inputs({"content": ""})
        response = self.make_post_request(
            reverse("create_answer", args=[self.question.id]), data
        )
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated(self):
        """
        To make sure that the answer is not created if the user is not authenticated
        """
        self.client.logout()
        response = self.make_post_request(
            reverse("create_answer", args=[self.question.id]), self.get_valid_inputs()
        )
        self.assertEqual(response.status_code, 302)  # Redirects to login


class AnswerUpdateTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.create_user()
        self.question = Question.objects.create(
            title=self.faker.sentence(),
            content=self.faker.paragraph(),
            author=self.create_user(),
        )
        self.answer = Answer.objects.create(
            content=self.faker.paragraph(), author=self.user, question=self.question
        )
        self.authenticate(self.user)
        self.update_valid_input()

    def update_valid_input(self):
        """
        This function is responsible for updating the valid inputs and
        creating data in databases as required
        """
        self.persisted_valid_inputs = {
            "content": self.faker.paragraph(),
        }

    def test_template(self):
        """
        To make sure that the correct template is used
        """
        response = self.make_get_request(
            reverse("update_answer", args=[self.answer.id])
        )
        self.assertTemplateUsed(response, "qna/update_answer.html")

    def test_success(self):
        """
        To make sure that the answer is updated successfully
        """
        data = self.get_valid_inputs()
        response = self.make_post_request(
            reverse("update_answer", args=[self.answer.id]), data
        )
        self.assertEqual(response.status_code, 302)
        self.answer.refresh_from_db()
        self.assertEqual(self.answer.content, data["content"])

    def test_failure(self):
        """
        To make sure that the answer is not updated if the data is invalid
        """
        data = self.get_valid_inputs({"content": ""})
        response = self.make_post_request(
            reverse("update_answer", args=[self.answer.id]), data
        )
        self.assertEqual(response.status_code, 200)

    def test_unauthorized(self):
        """
        To make sure that only the author can update the answer
        """
        other_user = self.create_user()
        self.authenticate(other_user)
        response = self.make_post_request(
            reverse("update_answer", args=[self.answer.id]), self.get_valid_inputs()
        )
        self.assertEqual(response.status_code, 404)


class AnswerDeleteTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.create_user()
        self.question = Question.objects.create(
            title=self.faker.sentence(),
            content=self.faker.paragraph(),
            author=self.create_user(),
        )
        self.answer = Answer.objects.create(
            content=self.faker.paragraph(), author=self.user, question=self.question
        )
        self.authenticate(self.user)

    def test_success(self):
        """
        To make sure that the answer is deleted successfully
        """
        response = self.make_post_request(
            reverse("delete_answer", args=[self.answer.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Answer.objects.filter(id=self.answer.id).exists())

    def test_unauthorized(self):
        """
        To make sure that only the author can delete the answer
        """
        other_user = self.create_user()
        self.authenticate(other_user)
        response = self.make_post_request(
            reverse("delete_answer", args=[self.answer.id])
        )
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Answer.objects.filter(id=self.answer.id).exists())
