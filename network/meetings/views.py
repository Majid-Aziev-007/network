from django.shortcuts import render, get_object_or_404
from .models import Meeting, Topic

def index(request):
    meeting_list = Meeting.objects.all().order_by('-pub_date')

    context = {
        'meeting_list': meeting_list
    }

    return render(request, 'meetings/index.html', context)

def topic_meetings(request, slug):

    topic = get_object_or_404(Topic, slug=slug)
    meeting_list = Meeting.objects.filter(topic=topic).order_by('-pub_date')[:10]

    context = {
        'topic': topic,
        'meeting_list': meeting_list,
    }
    return render(request, 'meetings/meetings_list.html', context) 
