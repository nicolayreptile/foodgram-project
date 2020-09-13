from django.contrib.auth import get_user_model

from rest_framework import serializers

from apps.main.models import Recipe
from apps.main.models import Ingredient

from apps.users.models import Favorite
from apps.users.models import Follow
from apps.users.models import ShopList
from apps.users.anonimous_shop_list import AnonimousShopList


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
        queryset=Recipe.objects.all()
    )

    class Meta:
        model = Favorite
        fields = ['recipe']


class FollowSerializer(serializers.ModelSerializer):

    author = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all()
    )

    class Meta:
        model = Follow
        fields = ['author']


class ShopListSerializer(serializers.ModelSerializer):

    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all()
    )

    class Meta:
        model = ShopList
        fields = ['recipe']


class AnonimousShopListSerializer:

    def __init__(self, request):
        self.shop_list = AnonimousShopList(request)
        self.data = request.data
        self.recipe_id = None

    def is_valid(self, raise_exception=False):
        recipe_id = self.data.get('recipe')
        recipe_exists = Recipe.objects.filter(pk=recipe_id).exists()
        if raise_exception:
            if not (recipe_id and recipe_exists):
                raise serializers.ValidationError('Recipe not found')
        if recipe_exists:
            self.recipe_id = recipe_id

    def save(self, *args, **kwargs):
        self.shop_list.add(self.recipe_id)
        self.data = {
            'recipe': self.recipe_id,
        }
