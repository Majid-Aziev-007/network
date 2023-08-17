from django.shortcuts import render, get_object_or_404, redirect
from .models import Meeting, Topic, Presence
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from .forms import MeetingForm
from customers.models import Key
from subscription.models import Subscribe
import random
import datetime

User = get_user_model()

def index(request):
    meeting_list = Meeting.objects.all().order_by('-pub_date')

    paginator = Paginator(meeting_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }

    return render(request, 'meetings/index.html', context)

def topic_meetings(request, slug):

    topic = get_object_or_404(Topic, slug=slug)
    meeting_list = Meeting.objects.filter(topic=topic).order_by('-pub_date')[:10]

    paginator = Paginator(meeting_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }

    context = {
        'topic': topic,
        'page_obj': page_obj,
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
def meeting_create(request):
    if request.user.get_group_permissions():
        form = MeetingForm(request.POST, files=request.FILES or None)
        if request.method == 'POST':
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                form.save()

                return redirect('meetings:index')

            return render(request, 'meetings/create_meeting.html', {'form': form})

        context = {
            'form': form,
        }

        return render(request, 'meetings/create_meeting.html', context)

    return render(request, 'meetings/index.html', context)

@login_required
def meeting_presence(request, meeting_id):

    if Subscribe.objects.filter(user=request.user):
        date_start = Subscribe.objects.filter(user=request.user)[0].date_start
        if (date_start + datetime.timedelta(days=32)).timestamp() < datetime.datetime.today().timestamp():
            Subscribe.objects.all().filter(user=request.user).delete()
            return redirect('customers:profile')

        meeting = get_object_or_404(Meeting, pk=meeting_id)

        key = str(random.randint(1000000000000000000000, 9999999999999999999999))
        link = "https://network-place.ru/profile/key-valid/" + key

        Key.objects.get_or_create(key=key, link=link, user=request.user, meeting=meeting)

        Presence.objects.get_or_create(user=request.user, meeting=meeting)

        return redirect('customers:profile')
    
    else:
        return redirect('subscription:page_buy')

@login_required
def meeting_not_presence(request, meeting_id):

    user = get_object_or_404(User, username=request.user.username)
    meeting = get_object_or_404(Meeting, pk=meeting_id)

    get_object_or_404(Presence, user=user, meeting=meeting).delete()
    Key.objects.all().filter(user=user, meeting=meeting).delete()

    return redirect('customers:profile')
