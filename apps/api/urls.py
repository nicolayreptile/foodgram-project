from django.urls import path

from apps.api.views import IngredientList
from apps.api.views import FavoriteHandler
from apps.api.views import FollowHandler
from apps.api.views import ShopListHandler


urlpatterns = [
    path('v1/ingredient/list/<str:query>', IngredientList.as_view()),
    path('v1/favorites/', FavoriteHandler.as_view()),
    path('v1/favorites/<recipe>/', FavoriteHandler.as_view()),
    path('v1/follow/', FollowHandler.as_view()),
    path('v1/follow/<author>/', FollowHandler.as_view()),
    path('v1/shoplist/', ShopListHandler.as_view()),
    path('v1/shoplist/<recipe>/', ShopListHandler.as_view()),

]
