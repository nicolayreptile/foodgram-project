from django.urls import path, include
from apps.users.views import UserSignup
from apps.users.views import UserFavorites
from apps.users.views import UserProfile
from apps.users.views import UserFollows
from apps.users.views import UserShopList

from django.contrib.auth import urls as auth_urls


urlpatterns = [
    path('signup', UserSignup.as_view(), name='signup'),
    path('favorites', UserFavorites.as_view(), name='favorites'),
    path('follows', UserFollows.as_view(), name='follows'),
    path('shoplist', UserShopList.as_view(), name='shoplist'),
    path('profile/<str:username>/', UserProfile.as_view(), name='profile'),
    path('', include(auth_urls))    
]
