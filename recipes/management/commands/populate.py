from django.core.management.base import BaseCommand
from recipes.models import Category, Recipe
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.files.base import ContentFile
import random
import requests
from io import BytesIO

class Command(BaseCommand):
    help = 'Add images to existing recipes'

    def handle(self, *args, **options):
        recipes = Recipe.objects.all()
        for i, recipe in enumerate(recipes):
            # Download a random image from Lorem Picsum
            image_url = f'https://picsum.photos/400/300?random={i}'
            try:
                response = requests.get(image_url, timeout=10)
                if response.status_code == 200:
                    image_content = ContentFile(response.content)
                    cover_name = f'recipe_{recipe.id}.jpg'
                    recipe.cover.save(cover_name, image_content, save=True)
                    self.stdout.write(self.style.SUCCESS(f'Added image to recipe: {recipe.title}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Failed to download image for {recipe.title}'))
            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(f'Error downloading image for {recipe.title}: {e}'))