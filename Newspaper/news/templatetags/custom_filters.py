from django import template
import re

register = template.Library()

BAD_WORDS = (
    'редиска',
    'папаха',
    'папахе',
    'загон',
    'загоне',
    'лошадь',
    'лошадью',
    'лошади',
    'лошадям',
    'конюшня',
    'конюшне',
    'конюшней',

)


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(value):
    text = re.split(" |,", value)
    for index, item in enumerate(text):
        if item.lower() in BAD_WORDS:
            text[index] = text[index][0] + '****'
    text2 = ' '.join(text)
    return text2
