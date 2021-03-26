from django.test import TestCase, Client

from recipe.models import Recipe
from users.forms import User


class TestLoginCreateEditRecipe(TestCase):
    def setUp(self):
        """ create logged in author """
        self.logged_in_author = Client()
        self.author = User.objects.create_user(username="logged",
                                               email='test@test.ru',
                                               password='123454')
        self.logged_in_author.force_login(self.author, backend=None)

    def test_true(self):
        self.assertTrue(True)