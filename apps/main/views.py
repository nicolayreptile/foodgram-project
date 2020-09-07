from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.forms import inlineformset_factory

from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy

from apps.main.models import Ingredient
from apps.main.models import Recipe, RecipeIngredients
from apps.main.forms import RecipeForm

from apps.users.models import Favorite
from apps.users.models import Follow

class RecipeList(ListView):
    model = Recipe
    queryset = Recipe.objects.prefetch_related('tags')
    context_object_name = 'recipes'
    template_name = 'pages/index.html'
    
        
class RecipeNew(LoginRequiredMixin, CreateView):
    form_class = RecipeForm
    template_name = 'pages/recipe/new.html'
    login_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = inlineformset_factory(Ingredient, Recipe.ingredients.through, form=RecipeForm)
        return context        
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class RecipeDetail(DetailView):
    model = Recipe
    queryset = Recipe.objects.all()
    template_name = 'pages/recipe/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['in_favorite'] = Favorite.objects.filter(user=self.request.user, recipe=self.object).exists()
        context['in_followings'] = Follow.objects.filter(user=self.request.user, author=self.object.author).exists()
        return context
    