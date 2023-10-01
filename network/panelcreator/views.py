from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from meetings.models import Meeting, Presence
from .models import Creator

@login_required
def panel(request):
    """
        Панель Креатора
    """
    
    creator = Creator.objects.filter(user=request.user).exists()

    if creator:

        creator = get_object_or_404(Creator, user=request.user)

        meetings = Meeting.objects.filter(author=request.user)
        
        earned = 0

        for meeting in meetings:
            presence_count_meeting = Presence.objects.filter(meeting=meeting).count()
            meeting.np_panel = presence_count_meeting
            money = int(meeting.price) * int(presence_count_meeting)
            earned += money

        percentage_of_earned = (int(creator.percentage_of_earnings) * 0.01) * earned
        paid = creator.paid

        context = {
            'meetings': meetings,
            'earned': earned,
            'percentage_of_earned': percentage_of_earned,
            'paid': paid,
        }

        return render(request, 'panelcreator/panel.html', context)

    else:

        return render(request, 'meetings/index.html')
