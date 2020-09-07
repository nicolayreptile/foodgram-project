from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from django.urls import reverse_lazy

from apps.main.models import Recipe
from apps.main.models import Ingredient
from apps.users.forms import UserSignupForm
from apps.users.models import Favorite
from apps.users.models import Follow


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
        qs = Recipe.objects.filter(in_favorites__user=self.request.user)
        return qs

     
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
    

class UserShopList(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = 'pages/user/shoplist.html'
    context_object_name = 'shoplist'