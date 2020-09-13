from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from apps.api.views import RecipeViewSet
from apps.api.views import IngredientList
from apps.api.views import FavoriteHandler
from apps.api.views import FollowHandler
from apps.api.views import ShopListHandler

router = DefaultRouter()
router.register(r'recipes/', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('v1', include(router.urls)),
    path('v1/ingredient/list/<str:query>', IngredientList.as_view()),
    path('v1/favorites/', FavoriteHandler.as_view()),
    path('v1/favorites/<recipe>/', FavoriteHandler.as_view()),
    path('v1/follow/', FollowHandler.as_view()),
    path('v1/follow/<author>/', FollowHandler.as_view()),
    path('v1/shoplist/', ShopListHandler.as_view()),
    path('v1/shoplist/<recipe>/', ShopListHandler.as_view()),
    
]
