from django.contrib.auth import get_user_model
from django.db import models

from apps.main.models import Recipe


User = get_user_model()


class UserProfile(User):
    pass


class Follow(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        unique_together = ('user', 'author')


class Favorite(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='in_favorites')

    class Meta:
        unique_together = ('user', 'recipe')


class ShopList(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shop_list')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='in_shop_list')

    class Meta:
        unique_together = ('user', 'recipe')
