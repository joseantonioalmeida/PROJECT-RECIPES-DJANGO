from rest_framework.response import Response
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination


class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 2

class RecipeAPIv2List(ListCreateAPIView):
    queryset = Recipe.objects.get_published() #type:ignore
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination


class RecipeAPIv2Detail(RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.get_published() #type:ignore
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination

    def patch(self, request, *args, **kwargs):
        recipe = self.get_queryset().filter(pk=kwargs.get('pk')).first()
        serializer = RecipeSerializer(
            instance=recipe,
            data=request.data,
            many=False,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
        )