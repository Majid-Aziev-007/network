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
    """Главная Страница"""

    search_query = request.GET.get('search', '')

    if search_query:
        meeting_list = Meeting.objects.filter(address__icontains=search_query).order_by('-pub_date')

    else:
        # Список нетворкингов
        meeting_list = Meeting.objects.all().order_by('-pub_date')

    paginator = Paginator(meeting_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query
    }

    return render(request, 'meetings/index.html', context)

def topic_meetings(request, slug):
    """
        Распределение по темам Нетворки
        slug - Слаг топика
    """

    search_query = request.GET.get('search', '')

    # Получение нетворкингов по определенной теме
    topic = get_object_or_404(Topic, slug=slug)

    if search_query:
        meeting_list = Meeting.objects.filter(topic=topic, address__icontains=search_query).order_by('-pub_date')

    else:
        meeting_list = Meeting.objects.filter(topic=topic).order_by('-pub_date')

    paginator = Paginator(meeting_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'topic': topic,
        'page_obj': page_obj,
    }

    return render(request, 'meetings/meetings_list.html', context) 

def meeting_detail(request, meeting_id):
    """
        Детальнее про Нетворк
        meeting_id - ID Нетворка
    """

    # Получение нетворкинга детальнее
    meeting = get_object_or_404(Meeting, pk=meeting_id)

    # Получение числа присутствующих
    presence_quantity = Presence.objects.filter(meeting=meeting).all().count()

    # Проверка аутификации пользователя
    if request.user.is_authenticated:

        # Проверяем Наличие подписки
        if (not Subscribe.objects.filter(user=request.user)) and (meeting.type == "ON"):
            meeting.address = "*************"

        # Находим присутсвие его в нетворкингах
        presence = Presence.objects.filter(
            user=User.objects.get(username=request.user.username),
            meeting=meeting
        ).exists()

    else:
        presence = None

        # Проверка, что Нетворк онлайн
        if meeting.type == "ON":
            meeting.address = "*************"

    context = {
        'meeting': meeting,
        'presence': presence,
        'presence_quantity': presence_quantity
    }

    return render(request, 'meetings/meeting_detail.html', context)

@login_required
def meeting_create(request):
    """
        Создание Нетворка
    """

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
    """
        Отправить участие в нетворкинге
        meeting_id - ID Нетворкинга
    """

    # Проверка Подписки у пользователя
    if Subscribe.objects.filter(user=request.user):
        # Дата Начала подписки
        date_start = Subscribe.objects.filter(user=request.user)[0].date_start

        # Дата Конца подписки
        date_finish = date_start + datetime.timedelta(days=32)

        # Сегодняшняя Дата
        today_date = datetime.datetime.today()

        # Проверка срока годности подписки
        if date_finish.timestamp() < today_date.timestamp():
            Subscribe.objects.all().filter(user=request.user).delete()
            return redirect('customers:profile')

        # Получение Нетворкинга
        meeting = get_object_or_404(Meeting, pk=meeting_id)

        # Генерация Ключа
        key = str(random.randint(1000000000000000000000, 9999999999999999999999))
        link = "https://network-place.ru/profile/key-valid/" + key

        # Создание Ключа
        Key.objects.get_or_create(key=key, link=link, user=request.user, meeting=meeting)

        # Создание Присутствия
        Presence.objects.get_or_create(user=request.user, meeting=meeting)

        return redirect('customers:profile')
    
    else:

        return redirect('subscription:page_buy')

@login_required
def meeting_not_presence(request, meeting_id):
    """
        Отправить отсутствие в нетворкинге
        meeting_id - ID Нетворкинга
    """

    # Получение Юзера
    user = get_object_or_404(User, username=request.user.username)

    # Получение Нетворкинга
    meeting = get_object_or_404(Meeting, pk=meeting_id)

    # Удаление Присутствия
    get_object_or_404(Presence, user=user, meeting=meeting).delete()

    # Удаление Ключа
    Key.objects.all().filter(user=user, meeting=meeting).delete()

    return redirect('customers:profile')
