from django.shortcuts import render
from meetings.models import Presence
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):

    meetings = Presence.objects.filter(user=request.user)

    paginator = Paginator(meetings, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'customers/profile.html', context)
