from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


class Tag(models.Model):    
    name = models.CharField('Название', max_length=254)
    
    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'
        
    def __str__(self):
        return self.name


class Unit(models.Model):
    ''' Единицы измерения, пока что не используются '''
    name = models.CharField('Название', max_length=254)
    
    class Meta:
        verbose_name = 'единица измерения'
        verbose_name_plural = 'единицы измерения'
        
    def __str__(self):
        return self.name


class Ingredient(models.Model):    
    name = models.CharField('Наименование', db_index=True, max_length=254, unique=True)
    unit = models.CharField('Единица измеерния', max_length=63)
    
    class Meta:
        verbose_name = 'ингридиент'
        verbose_name_plural = 'ингридиенты'
    
    def __str__(self):
        return self.name


class Recipe(models.Model):
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user_recipes', null=True)
    title = models.CharField('Название', db_index=True, max_length=254)
    description = models.TextField('Описание', blank=True, null=False)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredients')
    tags = models.ManyToManyField(Tag, related_name='recipes', null=True)
    image = models.ImageField('Изображение', upload_to='images', null=True)
    cook_time = models.TimeField('Время приготовления')
    slug = models.SlugField('Адрес в адресной строке')
    created_at = models.DateTimeField('Дата/время создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата/время последенго редактироваия', auto_now=True)
    
    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
        ordering = ('-created_at', '-updated_at', )
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("recipe_detail", kwargs={"pk": self.pk})


class RecipeIngredients(models.Model):
    
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='recipes')
    quantity = models.IntegerField('Количество')

