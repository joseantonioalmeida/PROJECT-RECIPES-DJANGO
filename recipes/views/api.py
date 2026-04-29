from rest_framework.response import Response
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet


class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 2

class RecipeAPIv2ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published() #type:ignore
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination

    def partial_update(self, request, *args, **kwargs):
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