from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.views import View
from django.views.generic import CreateView, DetailView, ListView
from django.urls import reverse_lazy

from apps.main.models import Ingredient, Recipe
from apps.users.anonimous_shop_list import AnonimousShopList
from apps.users.forms import UserSignupForm
from apps.users.models import Follow
from apps.users.helpers import ShopListToPdf


class UserSignup(CreateView):
    form_class = UserSignupForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


class UserProfile(DetailView):
    model = get_user_model()
    template_name = 'pages/user/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipes'] = Recipe.objects.filter(author=context['author'])
        if self.request.user.is_authenticated:
            context['in_followings'] = Follow.objects.filter(user=self.request.user, author=context['author'])
        return context


class UserFavorites(LoginRequiredMixin, ListView):

    template_name = 'pages/user/favorites.html'
    context_object_name = 'recipes'
    model = Recipe

    def get_queryset(self):
        qs = Recipe.objects.filter(in_favorites__user=self.request.user).prefetch_related('in_shop_list')
        exclude_tags = self.request.GET.getlist('exclude')
        if exclude_tags:
            exclude_tags = list(map(int, exclude_tags))
            qs = qs.exclude(tags__pk__in=exclude_tags)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_shop_list'] = (
            self.request.user.shop_list
            .filter(recipe__in=context['recipes'])
            .values_list('recipe', flat=True)
        )
        return context


class UserFollows(LoginRequiredMixin, ListView):

    template_name = 'pages/user/follows.html'
    context_object_name = 'follows'
    model = Follow

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        follow = Follow.objects.select_related('author').filter(user=self.request.user)
        recipes = Recipe.objects.filter(author__in=follow.values('author'))
        User = get_user_model()
        authors = User.objects.filter(pk__in=follow.values('author'))

        context['follows'] = []
        for author in authors:
            context['follows'].append({
                'author': author,
                'recipes': recipes.filter(author=author)[:3]
            })

        return context


class UserShopList(ListView):
    model = Ingredient
    template_name = 'pages/user/shoplist.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            qs = Recipe.objects.filter(in_shop_list__user=self.request.user)
        else:
            shop_list = AnonimousShopList(self.request)
            qs = Recipe.objects.filter(pk__in=shop_list.items)
        exclude_tags = self.request.GET.getlist('exclude')

        if exclude_tags:
            exclude_tags = list(map(int, exclude_tags))
            qs = qs.exclude(tags__pk__in=exclude_tags)

        return qs


class UserShopListPdf(View):

    def get(self, request, *args, **kwargs):
        shop_list_to_pdf = ShopListToPdf(request)
        pdf = shop_list_to_pdf.get_pdf()
        return FileResponse(pdf, as_attachment=True, filename='shop_list.pdf', )
