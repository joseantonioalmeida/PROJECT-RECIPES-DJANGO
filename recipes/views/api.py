from rest_framework.decorators import api_view
from rest_framework.response import Response
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView


class RecipeAPIv2List(APIView):
    def get(self, request):
        recipes = Recipe.objects.get_published()[:20] #type:ignore
        serializer = RecipeSerializer(instance=recipes, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = RecipeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author_id=1, category_id=3)

        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED
        )
    
class RecipeAPIv2Detail(APIView):
    def get_recipe(self, pk):
        recipe = get_object_or_404(
            Recipe.objects.get_published(), #type:ignore
            pk=pk,
        )
        return recipe
    
    def get(self, request, pk):
        recipe = self.get_recipe(pk)
        serializer = RecipeSerializer(instance=recipe, many=False)
        return Response(serializer.data)
    
    def patch(self, request, pk):
        recipe = self.get_recipe(pk)
        serializer = RecipeSerializer(
            instance=recipe, data=request.data, 
            many=False, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, pk):
        recipe = self.get_recipe(pk)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
