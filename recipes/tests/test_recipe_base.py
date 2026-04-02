from django.test import TestCase
from recipes import models
from django.contrib.auth.models import User

class RecipeTestBase(TestCase):
    # o  metodo setUp é chamado antes de cada teste
    def setUp(self) -> None:
        # todos os testes terá essa receita
        category = models.Category.objects.create(name='Category Test')
        author = User.objects.create_user(
            first_name='user',
            last_name='user',
            username='user',
            password='user',
            email='user',
        )
        recipe = models.Recipe.objects.create(
            category=category,
            author=author,
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
            preparation_steps_is_html=False,
            is_published=True,
        )
        return super().setUp()
