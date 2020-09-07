from django.contrib.auth import get_user_model
from django.views.generic import TemplateView

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


from apps.main.models import Recipe
from apps.main.models import Ingredient

from apps.users.models import Favorite
from apps.users.models import Follow
from apps.users.models import ShopList


class RecipeSerializer(serializers.ModelSerializer):
    
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')
    
    class Meta:
        model = Recipe
        fields = '__all__'
        

class IngredientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ingredient
        fields = '__all__'
        
        
class FavoriteSerializer(serializers.ModelSerializer):
    
    recipe = serializers.PrimaryKeyRelatedField(
        queryset = Recipe.objects.all()
    )

    class Meta:
        model = Favorite
        fields = ['recipe']
        

class FollowSerializer(serializers.ModelSerializer):
    
    author = serializers.PrimaryKeyRelatedField(
        queryset = get_user_model().objects.all()
    )

    class Meta:
        model = Follow
        fields = ['author']
        

class ShopListSerializer(serializers.ModelSerializer):
    
    recipe = serializers.PrimaryKeyRelatedField(
        queryset = Recipe.objects.all()
    )

    class Meta:
        model = ShopList
        fields = ['recipe']