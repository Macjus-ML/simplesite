from django.forms import ModelForm, DecimalField
from django.forms.widgets import Select

from .models import Bb


class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric')
        labels = {'title': 'Название товара '}
        help_texts = {'rubric': 'Не забудьте выбрать рубрику'}
        field_classes = {'price': DecimalField}
        widgets = {'rubrics': Select(attrs={'size': 8})}
