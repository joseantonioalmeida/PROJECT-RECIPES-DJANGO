from rest_framework import serializers
from recipes.models import Recipe
from authors.validators import AuthorRecipeValidator

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'public', 'preparation', 'author', 
                  'category', 'preparation_time', 'preparation_time_unit', 'servings', 
                  'servings_unit','preparation_steps', 'cover'
        ]
    public = serializers.BooleanField(source='is_published', read_only=True)
    preparation = serializers.SerializerMethodField(
        method_name='any_method_name', read_only=True,
    )
    category = serializers.StringRelatedField(read_only=True)
    author = serializers.StringRelatedField(read_only=True)

    def any_method_name(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'
    
    def validate(self, attrs):
        super_validate =  super().validate(attrs)
        AuthorRecipeValidator(data=attrs, ErrorClass=serializers.ValidationError)
        return super_validate
    
    def save(self, **kwargs):
        return super().save(**kwargs)