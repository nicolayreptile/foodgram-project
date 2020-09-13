from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.main.views import RecipeList
from apps.main.views import RecipeNew
from apps.main.views import RecipeDetail
from apps.main.views import RecipeUpdate


router = DefaultRouter()

urlpatterns = [
    path('', RecipeList.as_view(), name='index'),
    path('recipe/new', RecipeNew.as_view(), name='recipe_new'),
    path('recipe/<pk>/', RecipeDetail.as_view(), name='recipe_detail'),
    path('recipe/<pk>/update', RecipeUpdate.as_view(), name='recipe_update')
]
