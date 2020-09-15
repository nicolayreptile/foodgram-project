from django.urls import path

from apps.main.views import (
    AboutPage,
    RecipeDetail,
    RecipeList,
    RecipeNew,
    RecipeUpdate,
    TechnologiesPage
)


urlpatterns = [
    path('', RecipeList.as_view(), name='index'),
    path('recipe/new', RecipeNew.as_view(), name='recipe_new'),
    path('recipe/<int:pk>/', RecipeDetail.as_view(), name='recipe_detail'),
    path('recipe/<int:pk>/update', RecipeUpdate.as_view(), name='recipe_update'),
    path('about/', AboutPage.as_view(), name='about'),
    path('technologies/', TechnologiesPage.as_view(), name='technologies')
]
