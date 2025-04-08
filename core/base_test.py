from django.db.models import Q
from django.http import QueryDict
from django.test import Client, TestCase
from faker import Faker
from model_bakery import baker

from accounts.models import User


class BaseTestCase(TestCase):

    persisted_valid_inputs = {}

    def setUp(self):
        """
        This function will be called before the start of every test
        """
        self.client = Client()
        self.faker = Faker()

    def create_user(self):
        """
        This function is responsible for creating an user and giving
        them admin access
        """
        user = baker.make(
            User,
            _fill_optional=["email"],
        )
        return user

    def authenticate(self, user=None):
        """
        This function is responsible for authenticating the created user
        """
        if not user:
            user = self.create_user()
        self.client.force_login(user)

    def make_get_request(self, url_pattern, data=None):
        """
        This function is responsible for handling the GET requests
        """
        return self.client.get(url_pattern, data=data)

    def make_post_request(self, url_pattern, data=None):
        """
        This function is responsible for handling the POST requests
        """
        return self.client.post(url_pattern, data)

    def make_delete_request(self, url_pattern, data=None):
        """
        This function is responsible for handling DELETE requests}
        """
        return self.client.delete(url_pattern, data)

    def get_valid_inputs(self, override={}):
        """
        This function is responsible for getting the valid inputs for
        testcases and updating it as per need
        """
        query_dict = QueryDict("", mutable=True)
        query_dict.update({**self.persisted_valid_inputs, **override})
        return query_dict

    def get_queryset_instance(self, model, filters):
        """
        This function is responsible for filtering the model
        as per the need
        """
        query_filters = Q(**filters)
        return model.objects.filter(query_filters)

    def assert_database_has(self, model, filters):
        """
        This function checks whether the DB has the data which
        we have created or manipulated
        """
        queryset = self.get_queryset_instance(model, filters)
        self.assertTrue(queryset.exists())
