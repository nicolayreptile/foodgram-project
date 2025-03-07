from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from apps.main.forms import RecipeForm
from apps.main.models import Recipe, Tag
from apps.users.models import Favorite, Follow, ShopList
from apps.users.anonimous_shop_list import AnonimousShopList


class RecipeList(ListView):
    model = Recipe
    queryset = Recipe.objects.prefetch_related('tags')
    context_object_name = 'recipes'
    template_name = 'pages/index.html'
    paginate_by = 6

    def get_queryset(self):
        qs = super().get_queryset()
        exclude_tags = self.request.GET.get('exclude')
        if exclude_tags:
            try:
                include = Tag.objects.exclude(pk__in=list(exclude_tags))
                qs = qs.filter(tags__in=include).distinct()
            except ValueError:
                raise Http404
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_shop_list'] = self.request.user.shop_list.filter(
                recipe__in=context['recipes']
            ).values_list('recipe', flat=True)
            context['user_favorites'] = self.request.user.favorites.filter(
                recipe__in=context['recipes']
            ).values_list('recipe', flat=True)
        else:
            shop_list = AnonimousShopList(self.request)
            context['user_shop_list'] = shop_list.items
        return context


class RecipeNew(LoginRequiredMixin, CreateView):
    form_class = RecipeForm
    template_name = 'pages/recipe/new.html'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        self.object = form.save(user=self.request.user)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class RecipeUpdate(LoginRequiredMixin, UpdateView):
    form_class = RecipeForm
    model = Recipe
    template_name = 'pages/recipe/update.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients_with_quantity'] = self.get_object().get_ingredients_with_quantity()
        return context

    def dispatch(self, request, *args, **kwargs):
        recipe = self.get_object()
        if not recipe.author == request.user:
            return redirect('recipe_detail', pk=recipe.pk)
        return super().dispatch(request, *args, **kwargs)


class RecipeDetail(DetailView):
    queryset = (
        Recipe.objects.prefetch_related('ingredients').prefetch_related('tags')
    )
    template_name = 'pages/recipe/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients_with_quantity'] = self.get_object().get_ingredients_with_quantity()
        if self.request.user.is_authenticated:
            context['in_shop_list'] = ShopList.objects.filter(
                user=self.request.user, recipe=self.object
            ).exists()
            context['in_favorite'] = Favorite.objects.filter(
                user=self.request.user, recipe=self.object
            ).exists()
            context['in_followings'] = Follow.objects.filter(
                user=self.request.user, author=self.object.author
            ).exists()
        else:
            shop_list = AnonimousShopList(self.request)
            context['in_shop_list'] = self.get_object().pk in shop_list.items
        return context
