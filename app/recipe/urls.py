from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

router = DefaultRouter()  # automatic generate urls
router.register('tags', TagViewSet)
router.register('ingredient', IngredientViewSet)
router.register('recipe', RecipeViewSet)

app_name = 'recipe'

urlpatterns = [path('', include(router.urls))]
# all the generated url are registered
