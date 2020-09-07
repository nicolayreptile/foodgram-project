from django import forms
from django.forms.widgets import CheckboxInput
from apps.main.models import Ingredient
from apps.main.models import Recipe
from apps.main.models import Tag
from apps.main.models import Unit


class RecipeForm(forms.ModelForm):
    title = forms.CharField(
        label = 'Название рецепта',
        widget=forms.TextInput(attrs={
            'type': 'text',
            'id': "id_name",
            'name': 'title',
            'class': 'form__input',
        })
    )
    ingredients = forms.ModelMultipleChoiceField(
        label = 'Ингредиенты',
        queryset = Ingredient.objects.all()
        # widget = forms.MultiWidget(attrs={
        #     'type': 'text',
        #     'id': "nameIngredient",
        #     'class': 'form__input',
        #     'min': '0'
        # }),        
    )
    cook_time = forms.TimeField(
        label = 'Время приготовления',
        widget = forms.TimeInput(attrs={
            'type': 'text',
            'id': 'id_time',
            'name': 'cook_time',
            'class': 'form__input'
        })
    )
    tags = forms.ModelMultipleChoiceField(
        label = 'Тэги',
        widget = forms.CheckboxSelectMultiple(),
        queryset = Tag.objects.all()        
    )
    description = forms.CharField(
        label = 'Описание',
        widget = forms.Textarea(attrs={
            'id': 'id_description',
            'name': 'description',
            'class': 'form__textarea',
            'rows': '8'
        })
    )
    quantity = forms.CharField(
        label = 'Количество',
        widget = forms.NumberInput(attrs={
            'id': 'cantidad',
            'class': 'form__input',
            'min': '0'
        })
    )
    image = forms.ImageField(
        label = 'Загрузить фото',
        widget=forms.FileInput(attrs={
            'id': 'id_file',
            'type': 'file',
            'name': 'image',
            'class': 'form__file',
        })
    )
    class Meta:
        model = Recipe
        fields = ['title',
                  'tags', 
                  'ingredients',                
                  'cook_time',
                  'description',
                  'image']
        
 
class IngridientForm(forms.ModelForm):
    
    class Meta:
        model = Ingredient
        fields = ['name']