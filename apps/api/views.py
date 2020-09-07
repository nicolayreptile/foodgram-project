from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import ListModelMixin

from apps.api.serialaizers import RecipeSerializer
from apps.api.serialaizers import IngredientSerializer
from apps.api.serialaizers import FavoriteSerializer
from apps.api.serialaizers import FollowSerializer
from apps.api.serialaizers import ShopListSerializer
from apps.main.models import Ingredient
from apps.users.models import Favorite
from apps.users.models import Follow
from apps.users.models import ShopList

class RecipeViewSet(ModelViewSet):
    allowed_methods = ('GET', 'POST')
    #queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class IngredientList(ListAPIView):
    serializer_class = IngredientSerializer
    
    def get_queryset(request, *args, **kwargs): 
        query = request.kwargs.get('query')
        return Ingredient.objects.filter(name__contains=query)


class UserActivityBaseHandler(CreateModelMixin,
                      DestroyModelMixin,
                      GenericAPIView):
    model = None
    
    def get_queryset(self):
        qs = self.model.objects.filter(user=self.request.user)
        return qs
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    

class FavoriteHandler(UserActivityBaseHandler):
    
    model = Favorite
    serializer_class = FavoriteSerializer
    lookup_field = 'recipe'          


class FollowHandler(UserActivityBaseHandler):
    
    model = Follow
    serializer_class = FollowSerializer
    lookup_field = 'author'
        

class ShopListHandler(UserActivityBaseHandler):
    
    model = ShopList
    serializer_class = ShopListSerializer
    lookup_field = 'recipe'