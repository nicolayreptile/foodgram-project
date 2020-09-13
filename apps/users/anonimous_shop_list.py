from django.conf import settings


class AnonimousShopList:

    def __init__(self, request, *args, **kwargs):
        self.session = request.session
        shop_list = self.session.get(settings.SHOP_LIST_SESSION_ID)
        if not shop_list:
            shop_list = self.session[settings.SHOP_LIST_SESSION_ID] = []

        self.shop_list = shop_list

    def add(self, recipe_id):
        if recipe_id not in self.shop_list:
            self.shop_list.append(int(recipe_id))
            self.save()

    def remove(self, recipe_id):
        if recipe_id in self.shop_list:
            self.shop_list.remove(int(recipe_id))
            self.save()

    def save(self):
        self.session[settings.SHOP_LIST_SESSION_ID] = self.shop_list
        self.session.modified = True

    @property
    def count(self):
        return len(self.shop_list)

    @property
    def items(self):
        return self.shop_list

    def clear(self):
        self.shop_list.clear()
        self.save()
