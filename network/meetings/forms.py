from django.contrib.auth import get_user_model
from django.forms import ModelForm

from .models import Meeting


class MeetingForm(ModelForm):
    class Meta:

        model = Meeting

        fields = ('type', 'title', 'description', 'image',
                  'meeting_date', 'address', 'topic',
                  'price')
        labels = {'type' : 'Тип Встречи', 
                  'title': 'Название', 
                  'description': 'Описание', 
                  'image': 'Картинка',
                  'meeting_date': 'День Нетворка', 
                  'address': 'Адрес / Ссылка', 
                  'topic': 'Тематика',
                  'price': 'Цена'
                  }
