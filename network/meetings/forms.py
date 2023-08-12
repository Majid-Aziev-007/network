from django.contrib.auth import get_user_model
from django.forms import ModelForm

from .models import Meeting


class MeetingForm(ModelForm):
    class Meta:

        model = Meeting

        fields = ('type', 'title', 'description', 'meeting_date', 'address', 'topic')

