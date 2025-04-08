from django.urls import reverse
from django.contrib.auth import get_user_model
from core.base_test import BaseTestCase


class AuthenticationTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.create_user()
        self.update_valid_input()

    def update_valid_input(self):
        """
        This function is responsible for updating the valid inputs
        """
        self.persisted_valid_inputs = {
            "username": self.faker.user_name(),
            "email": self.faker.email(),
            "password1": "testpass123",
            "password2": "testpass123",
        }

    def test_login_template(self):
        """
        To make sure that the correct template is used for login
        """
        response = self.make_get_request(reverse("login"))
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_register_template(self):
        """
        To make sure that the correct template is used for registration
        """
        response = self.make_get_request(reverse("register"))
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_login_success(self):
        """
        To make sure that login works with correct credentials
        """
        data = self.get_valid_inputs()
        response = self.make_post_request(reverse("register"), data)  # Register the user
        response = self.make_post_request(
            reverse("login"),
            {
                "username": data["email"],
                "password": data["password1"]
            }
        )
        self.assertEqual(response.status_code, 302)  # Redirect to success URL
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_failure_wrong_password(self):
        """
        To make sure that login fails with wrong password
        """
        response = self.make_post_request(
            reverse("login"),
            {
                "username": self.user.username,
                "password": "wrongpass"
            }
        )
        self.assertEqual(response.status_code, 200)  # Stay on login page
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_failure_nonexistent_user(self):
        """
        To make sure that login fails with nonexistent user
        """
        response = self.make_post_request(
            reverse("login"),
            {
                "username": "nonexistentuser",
                "password": "testpass123"
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_register_success(self):
        """
        To make sure that registration works with valid data
        """
        data = self.get_valid_inputs()
        response = self.make_post_request(reverse("register"), data)
        self.assertEqual(response.status_code, 302)  # Redirect to success URL
        self.assertTrue(
            get_user_model().objects.filter(username=data["username"]).exists()
        )

    def test_register_failure_password_mismatch(self):
        """
        To make sure that registration fails when passwords don't match
        """
        data = self.get_valid_inputs({"password2": "differentpass"})
        response = self.make_post_request(reverse("register"), data)
        self.assertEqual(response.status_code, 200)  # Stay on register page
        self.assertFalse(
            get_user_model().objects.filter(username=data["username"]).exists()
        )

    def test_register_failure_existing_username(self):
        """
        To make sure that registration fails with existing username
        """
        data = self.get_valid_inputs({"username": self.user.username})
        response = self.make_post_request(reverse("register"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            get_user_model().objects.filter(username=self.user.username).count(),
            1
        )

    def test_register_failure_invalid_email(self):
        """
        To make sure that registration fails with invalid email
        """
        data = self.get_valid_inputs({"email": "invalid-email"})
        response = self.make_post_request(reverse("register"), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            get_user_model().objects.filter(username=data["username"]).exists()
        )

    def test_logout(self):
        """
        To make sure that logout works correctly
        """
        self.authenticate(self.user)
        response = self.make_post_request(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_redirect(self):
        """
        To make sure that unauthenticated users are redirected to login
        """
        response = self.make_get_request(reverse("create_question"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("login"))) 
