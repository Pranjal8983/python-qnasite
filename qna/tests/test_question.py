from django.urls import reverse

from core.base_test import BaseTestCase
from qna.models.question import Question


class QuestionCreateTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.create_user()
        self.authenticate(self.user)
        self.update_valid_input()

    def update_valid_input(self):
        """
        This function is responsible for updating the valid inputs and
        creating data in databases as reqiured
        """
        self.persisted_valid_inputs = {
            "title": self.faker.sentence(),
            "content": self.faker.paragraph(),
        }

    def test_template(self):
        """
        To makes sure that the correct template is used
        """
        response = self.make_get_request(reverse("create_question"))
        self.assertTemplateUsed(response, "qna/create_question.html")

    def test_success(self):
        """
        To makes sure that the question is created successfully
        """
        data = self.get_valid_inputs()
        response = self.make_post_request(reverse("create_question"), data)
        self.assertEqual(response.status_code, 302)

        self.assert_database_has(Question, {"title": data["title"]})

    def test_failure(self):
        """
        To makes sure that the question is not created if the data is invalid
        """
        data = self.get_valid_inputs({"title": ""})
        response = self.make_post_request(reverse("create_question"), data)
        self.assertEqual(
            response.status_code, 200
        )  # Status code 200 is returned for form errors

    def test_unauthenticated(self):
        """
        To makes sure that the question is not created if the user is not authenticated
        """
        response = self.make_post_request(
            reverse("create_question"), self.get_valid_inputs()
        )
        self.assertEqual(response.status_code, 302)


class QuestionUpdateTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.create_user()
        self.question = Question.objects.create(
            title="Test Question", content="Test Content", author=self.user
        )
        self.authenticate(self.user)
        self.update_valid_input()

    def update_valid_input(self):
        """
        This function is responsible for updating the valid inputs and
        creating data in databases as reqiured
        """
        self.persisted_valid_inputs = {
            "title": self.faker.sentence(),
            "content": self.faker.paragraph(),
        }

    def test_template(self):
        """
        To makes sure that the correct template is used
        """
        response = self.make_get_request(
            reverse("update_question", args=[self.question.id])
        )
        self.assertTemplateUsed(response, "qna/update_question.html")

    def test_success(self):
        """
        To makes sure that the question is updated successfully
        """
        data = self.get_valid_inputs()
        response = self.make_post_request(
            reverse("update_question", args=[self.question.id]), data
        )
        self.assertEqual(response.status_code, 302)
        self.assert_database_has(Question, {"title": data["title"]})

    def test_failure(self):
        """
        To makes sure that the question is not updated if the data is invalid
        """
        data = self.get_valid_inputs({"title": ""})
        response = self.make_post_request(
            reverse("update_question", args=[self.question.id]), data
        )
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated(self):
        """
        To makes sure that the question is not updated if the user is not authenticated
        """
        response = self.make_post_request(
            reverse("update_question", args=[self.question.id]), self.get_valid_inputs()
        )
        self.assertEqual(response.status_code, 302)


class QuestionDeleteTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.create_user()
        self.question = Question.objects.create(
            title="Test Question", content="Test Content", author=self.user
        )
        self.authenticate(self.user)

    def test_success(self):
        """
        To makes sure that the question is deleted successfully
        """
        response = self.make_post_request(
            reverse("delete_question", args=[self.question.id])
        )
        self.assertEqual(response.status_code, 302)

    def test_failure(self):
        """
        To makes sure that the question is not deleted if the user is not authenticated
        """
        response = self.make_post_request(
            reverse("delete_question", args=[self.question.id])
        )
        self.assertEqual(response.status_code, 302)

    def test_unauthenticated(self):
        """
        To makes sure that the question is not deleted if the user is not authenticated
        """
        response = self.make_post_request(
            reverse("delete_question", args=[self.question.id])
        )
        self.assertEqual(response.status_code, 302)
