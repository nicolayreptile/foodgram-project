from django.contrib import admin
from apps.main.models import Recipe

class RecipeAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Recipe, RecipeAdmin)
