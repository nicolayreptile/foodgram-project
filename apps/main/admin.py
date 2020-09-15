from django.contrib import admin

from apps.main.models import Ingredient, Recipe, Tag


class RecipeAdmin(admin.ModelAdmin):
    list_filter = ('title', )


class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('name', )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(Tag)
