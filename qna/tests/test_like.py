from django.urls import reverse

from core.base_test import BaseTestCase
from qna.models import Answer, Question


class LikeTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.create_user()
        self.other_user = self.create_user()
        self.question = Question.objects.create(
            title=self.faker.sentence(),
            content=self.faker.paragraph(),
            author=self.other_user,
        )
        self.answer = Answer.objects.create(
            content=self.faker.paragraph(),
            author=self.other_user,
            question=self.question,
        )
        self.authenticate(self.user)

    def test_like_answer(self):
        """
        To make sure that a user can like an answer
        """
        response = self.make_post_request(reverse("like_answer", args=[self.answer.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.answer.likes.filter(id=self.user.id).exists())

    def test_unlike_answer(self):
        """
        To make sure that a user can unlike an answer they previously liked
        """
        # First like the answer
        self.answer.likes.add(self.user)

        # Then unlike it
        response = self.make_post_request(reverse("like_answer", args=[self.answer.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.answer.likes.filter(id=self.user.id).exists())

    def test_like_own_answer(self):
        """
        To make sure that a user can like their own answer
        """
        own_answer = Answer.objects.create(
            content=self.faker.paragraph(), author=self.user, question=self.question
        )
        response = self.make_post_request(reverse("like_answer", args=[own_answer.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(own_answer.likes.filter(id=self.user.id).exists())

    def test_unauthenticated(self):
        """
        To make sure that unauthenticated users cannot like answers
        """
        self.client.logout()
        response = self.make_post_request(reverse("like_answer", args=[self.answer.id]))
        self.assertEqual(response.status_code, 302)  # Redirects to login
        self.assertFalse(self.answer.likes.filter(id=self.user.id).exists())
