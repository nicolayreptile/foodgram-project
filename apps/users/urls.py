from django.urls import path, include

from apps.users.views import (
    UserFavorites,
    UserFollows,
    UserProfile,
    UserSignup,
    UserShopList,
    UserShopListPdf
)

from django.contrib.auth import urls as auth_urls


urlpatterns = [
    path('signup', UserSignup.as_view(), name='signup'),
    path('favorites', UserFavorites.as_view(), name='favorites'),
    path('follows', UserFollows.as_view(), name='follows'),
    path('shoplist', UserShopList.as_view(), name='shoplist'),
    path('shoplist/download', UserShopListPdf.as_view(), name='shoplist_download'),
    path('profile/<slug:username>/', UserProfile.as_view(), name='profile'),
    path('', include(auth_urls))
]
