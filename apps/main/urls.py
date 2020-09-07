from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.api.views import RecipeViewSet
from apps.main.views import RecipeList
from apps.main.views import RecipeNew
from apps.main.views import RecipeDetail


router = DefaultRouter()

urlpatterns = [
    path('', RecipeList.as_view(), name='index'),
    path('recipe/new', RecipeNew.as_view(), name='recipe_new'),
    path('recipe/<pk>/', RecipeDetail.as_view(), name='recipe_detail')
]
