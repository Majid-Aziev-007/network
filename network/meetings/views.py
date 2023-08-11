from django.shortcuts import render, get_object_or_404, redirect
from .models import Meeting, Topic, Presence
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

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

def meeting_detail(request, meeting_id):

    meeting = get_object_or_404(Meeting, pk=meeting_id)
    presence_quantity = Presence.objects.filter(meeting=meeting).all().count()

    if request.user.is_authenticated:
        presence = Presence.objects.filter(
            user=User.objects.get(username=request.user.username),
            meeting=meeting
        ).exists()
    else:
        presence = None

    context = {
        'meeting': meeting,
        'presence': presence,
        'presence_quantity': presence_quantity
    }

    return render(request, 'meetings/meeting_detail.html', context)

@login_required
def meeting_presence(request, meeting_id):

    meeting = get_object_or_404(Meeting, pk=meeting_id)

    Presence.objects.get_or_create(user=request.user, meeting=meeting)

    return redirect('meetings:meeting_detail', meeting_id)

@login_required
def meeting_not_presence(request, meeting_id):

    user = get_object_or_404(User, username=request.user.username)
    meeting = get_object_or_404(Meeting, pk=meeting_id)

    get_object_or_404(Presence, user=user, meeting=meeting).delete()

    return redirect('meetings:meeting_detail', meeting_id)
