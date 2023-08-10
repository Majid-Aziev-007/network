from django.shortcuts import render
from .models import Meeting, Topic

def index(request):
    meeting_list = Meeting.objects.all().order_by('-pub_date')

    context = {
        'meeting_list': meeting_list
    }

    return render(request, 'meetings/index.html', context)
