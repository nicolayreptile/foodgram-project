from django import forms

from apps.main.models import Ingredient, Recipe, RecipeIngredients, Tag


class RecipeForm(forms.ModelForm):
    title = forms.CharField(
        label='Название рецепта',
        widget=forms.TextInput(attrs={
            'type': 'text',
            'id': "id_name",
            'name': 'title',
            'class': 'form__input',
        })
    )
    ingredients = forms.CharField(
        label='Ингредиенты',
        required=False,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'id': "nameIngredient",
            'class': 'form__input',
        }),
    )
    quantity = forms.IntegerField(
        label='Количество',
        required=False,
        widget=forms.NumberInput(attrs={
            'type': 'number',
            'id': 'cantidad',
            'class': 'form__input',
            'min': '0'
        })
    )
    cook_time = forms.TimeField(
        label='Время приготовления',
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'id': 'id_time',
            'name': 'cook_time',
            'class': 'form__input'
        })
    )
    tags = forms.ModelMultipleChoiceField(
        label='Тэги',
        widget=forms.CheckboxSelectMultiple(),
        queryset=Tag.objects.all()
    )
    description = forms.CharField(
        label='Описание',
        widget=forms.Textarea(attrs={
            'id': 'id_description',
            'name': 'description',
            'class': 'form__textarea',
            'rows': '8'
        })
    )
    image = forms.ImageField(
        label='Загрузить фото',
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

    def __init__(self, data=None, *args, **kwargs):
        if data is not None:
            data = data.copy()
            data.update({
                    'ingredients_ids': data.getlist('nameIngredient'),
                    'quantity_values': data.getlist('valueIngredient'),
                    'tags_ids': data.getlist('tags'),
            })
        self.ingredients_dict = None
        self.tags_ids = None
        super().__init__(data=data, *args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        ids = self.data['ingredients_ids']
        quantity = self.data['quantity_values']
        errors = []

        if not (ids and quantity):
            error = forms.ValidationError('Необходимо указать ингредиенты')
            self.add_error('ingredients', error)

        try:
            count = Ingredient.objects.filter(pk__in=ids).count()
            less_zero_quantity_values = [val for val in quantity if int(val) < 0]
            if less_zero_quantity_values:
                errors.append(forms.ValidationError('Отрицательное количество ингредиентов не может быть добавлено'))
            if not count == len(ids):
                raise ValueError
        except ValueError:
            errors.append(forms.ValidationError('В форму переданы некоректные данные. \
                Возможно, вы попытались добавить несуществующий ингредиент или ввели количество не в виде числа. \
                Не надо так.'))
        except:
            errors.append(forms.ValidationError('Произошла непредвиденная ошибка. Что-то вы ввели не так. \
                Попробуйте заполнить форму еще раз.'))

        for erorr in errors:
            self.add_error('ingredients', erorr)

        self.ingredients_dict = dict(zip(ids, quantity))
        self.tags_ids = self.data['tags_ids']

        return cleaned_data

    def save(self, *args, **kwargs):
        instance = super().save(commit=False)
        user = kwargs.get('user')
        if user is not None:
            instance.author = user
            instance.save()
        for pk, quantity in self.ingredients_dict.items():
            ingredient = Ingredient.objects.get(pk=pk)
            if not RecipeIngredients.objects.filter(recipe=instance, ingredient=ingredient).exists():
                ri = RecipeIngredients(
                    recipe=instance,
                    ingredient=ingredient,
                    quantity=quantity
                )
                ri.save()
        instance.tags.set(Tag.objects.filter(pk__in=self.tags_ids))
        instance.save()
        # self.save_m2m()
        return instance
