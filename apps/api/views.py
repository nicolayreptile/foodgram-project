from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from apps.api.serialaizers import RecipeSerializer
from apps.api.serialaizers import IngredientSerializer
from apps.api.serialaizers import FavoriteSerializer
from apps.api.serialaizers import FollowSerializer
from apps.api.serialaizers import ShopListSerializer
from apps.api.serialaizers import AnonimousShopListSerializer
    
from apps.main.models import Ingredient
from apps.main.models import Recipe
from apps.users.models import Favorite
from apps.users.models import Follow
from apps.users.models import ShopList
from apps.users.anonimous_shop_list import AnonimousShopList


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
    permission_classes = (IsAuthenticated, ) 


class FollowHandler(UserActivityBaseHandler):
    
    model = Follow
    serializer_class = FollowSerializer
    lookup_field = 'author'
    permission_classes = (IsAuthenticated, ) 
        

# class ShopListHandler(UserActivityBaseHandler):
    
#     model = ShopList
#     serializer_class = ShopListSerializer
#     lookup_field = 'recipe'
    
#     def get_serializer_class(self):
#         if not self.request.user.is_authenticated:
#             return AnonimousShopListSerializer
#         return super().get_serializer_class()

class ShopListHandler(APIView):
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            serializer = ShopListSerializer(data=request.data)            
        else:
            serializer = AnonimousShopListSerializer(request)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        
    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get('recipe')
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.user.is_authenticated:
            shop_list_item = get_object_or_404(ShopList, recipe=recipe, user=request.user)
            shop_list_item.delete()
        else:
            shop_list = AnonimousShopList(request)
            shop_list.remove(recipe.id)
        return Response(status=status.HTTP_204_NO_CONTENT)
            
