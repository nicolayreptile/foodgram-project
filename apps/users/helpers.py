import io
from datetime import datetime

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from apps.main.models import Recipe
from apps.users.anonimous_shop_list import AnonimousShopList


class ShopListToPdf:

    def __init__(self, request):
        self.for_username = 'гостя'
        if request.user.is_authenticated:
            recipes = Recipe.objects.filter(
                in_shop_list__user=request.user
            ).prefetch_related('ingredients')
            self.for_username = request.user.username
        else:
            shop_list = AnonimousShopList(request)
            recipes = Recipe.objects.filter(pk__in=shop_list.items)
        self.recipes = recipes

    def _get_items(self):
        items = {}
        for recipe in self.recipes:
            ingredients_with_quantity = recipe.get_ingredients_with_quantity()
            for item in ingredients_with_quantity:
                if items.get(item.ingredient.pk):
                    items[item.ingredient.pk][1] += item.quantity
                else:
                    items[item.ingredient.pk] = [item.ingredient.name, item.quantity, item.ingredient.unit]
        return items

    def get_pdf(self):
        items = self._get_items()
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, title=f'Список покупок для {self.for_username}')

        pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))

        sample_style_sheet = getSampleStyleSheet()
        heading_style = sample_style_sheet['Heading1']
        heading_style.fontName = 'FreeSans'
        body_style = sample_style_sheet['BodyText']
        body_style.fontName = 'FreeSans'

        flowtables = [
            Paragraph('Список покупок - Shopping list', heading_style)
        ]
        for index, item in enumerate(items.values(), start=1):
            string = f'{index}. {item[0]} ({item[2]}) - {item[1]}'
            flowtables.append(
                Paragraph(string, body_style)
            )

        flowtables.extend([
            Paragraph('', body_style),
            Paragraph(datetime.now().strftime('%d.%m.%Y %H:%M'), body_style)
        ])
        doc.build(flowtables)
        pdf_buffer.seek(0)

        return pdf_buffer
