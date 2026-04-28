from rest_framework.response import Response
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination


class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 2

class RecipeAPIv2List(ListCreateAPIView):
    queryset = Recipe.objects.get_published() #type:ignore
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination


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
