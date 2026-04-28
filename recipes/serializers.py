from rest_framework import serializers
from django.contrib.auth.models import User
from recipes.models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'public', 
                  'preparation', 'author', 'category'
        ]
    public = serializers.BooleanField(source='is_published', read_only=True)
    preparation = serializers.SerializerMethodField(
        method_name='any_method_name', read_only=True,
    )
    category = serializers.StringRelatedField(read_only=True)

    def any_method_name(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'