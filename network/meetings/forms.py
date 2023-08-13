from django.contrib.auth import get_user_model
from django.forms import ModelForm

from .models import Meeting


class MeetingForm(ModelForm):
    class Meta:

        model = Meeting

        fields = ('type', 'title', 'description', 
                  'meeting_date', 'address', 'topic')
        labels = {'type' : 'Тип Встречи', 
                  'title': 'Название', 
                  'description': 'Описание', 
                  'meeting_date': 'День Нетворка', 
                  'address': 'Адрес / Ссылка', 
                  'topic': 'Тематика'
                  }
