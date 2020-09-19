from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import FileResponse, Http404
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse_lazy

from apps.main.models import Recipe, Tag
from apps.users.anonimous_shop_list import AnonimousShopList
from apps.users.forms import UserSignupForm
from apps.users.models import Follow, User
from apps.users.helpers import ShopListToPdf


class UserSignup(CreateView):
    form_class = UserSignupForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


class UserProfile(ListView, SingleObjectMixin):
    template_name = 'pages/user/profile.html'
    context_object_name = 'recipes'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    paginate_by = 6

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=User.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.object
        if self.request.user.is_authenticated:
            context['in_followings'] = Follow.objects.filter(
                user=self.request.user, author=self.object)
            context['user_favorites'] = self.request.user.favorites.filter(
                recipe__in=context['recipes']
            ).values_list('recipe', flat=True)
            context['user_shop_list'] = self.request.user.shop_list.filter(
                recipe__in=context['recipes']
            ).values_list('recipe', flat=True)
        else:
            shop_list = AnonimousShopList(self.request)
            context['user_shop_list'] = shop_list.items
        return context

    def get_queryset(self):
        qs = Recipe.objects.prefetch_related(
                'tags'
                ).prefetch_related(
                'in_favorites'
                ).select_related(
                'author'
                ).filter(author=self.object)

        exclude_tags = self.request.GET.get('exclude')
        if exclude_tags:
            try:
                include = Tag.objects.exclude(pk__in=list(exclude_tags))
                qs = qs.filter(tags__in=include)
            except ValueError:
                raise Http404

        return qs


class UserFavorites(LoginRequiredMixin, ListView):
    template_name = 'pages/user/favorites.html'
    context_object_name = 'recipes'
    model = Recipe
    paginate_by = 6

    def get_queryset(self):
        qs = Recipe.objects.filter(
            in_favorites__user=self.request.user
        ).prefetch_related('in_shop_list')
        exclude_tags = self.request.GET.get('exclude')
        if exclude_tags:
            include = Tag.objects.exclude(pk__in=list(exclude_tags))
            qs = qs.filter(tags__in=include)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_shop_list'] = self.request.user.shop_list.filter(
            recipe__in=context['recipes']
            ).values_list('recipe', flat=True)
        return context


class UserFollows(LoginRequiredMixin, TemplateView):
    template_name = 'pages/user/follows.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page_num = self.request.GET.get('page', 1)

        authors = User.objects.filter(following__user=self.request.user)
        recipes = Recipe.objects.filter(author__in=authors)

        follows = []
        for author in authors:
            follows.append({
                'author': author,
                'recipes': recipes.filter(author=author)[:3]
            })
        paginator = Paginator(follows, 6)
        try:
            page_num = int(page_num)
        except ValueError:
            if page_num == 'last':
                page_num = paginator.num_pages
        except:
            raise Http404

        page_obj = paginator.page(page_num)

        context.update({
            'paginator': paginator,
            'page_obj': page_obj,
        })

        return context


class UserShopList(ListView):
    template_name = 'pages/user/shoplist.html'
    context_object_name = 'recipes'
    paginate_by = 6

    def get_queryset(self):
        if self.request.user.is_authenticated:
            qs = Recipe.objects.filter(in_shop_list__user=self.request.user)
        else:
            shop_list = AnonimousShopList(self.request)
            qs = Recipe.objects.filter(pk__in=shop_list.items)

        exclude_tags = self.request.GET.get('exclude')
        if exclude_tags:
            exclude_tags = list(exclude_tags)
            qs = qs.exclude(tags__pk__in=exclude_tags)

        return qs


class UserShopListPdf(View):

    def get(self, request, *args, **kwargs):
        shop_list_to_pdf = ShopListToPdf(request)
        pdf = shop_list_to_pdf.get_pdf()
        return FileResponse(pdf, as_attachment=True, filename='shop_list.pdf', )
