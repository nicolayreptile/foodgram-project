from apps.users.models import ShopList
from apps.users.anonimous_shop_list import AnonimousShopList

def shop_list_count(request):
    if request.user.is_authenticated:
        count = ShopList.objects.filter(user=request.user).count()
    else:
        shop_list = AnonimousShopList(request)
        count = shop_list.count
    return {
        'shop_list_count': count,
    }