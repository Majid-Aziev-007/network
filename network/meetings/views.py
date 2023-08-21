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
from datetime import date
from subscription.views import payurl
from yoomoney import Client

User = get_user_model()

def index(request):
    """Главная Страница"""

    # Список нетворкингов
    meeting_list = Meeting.objects.all().order_by('-pub_date')

    paginator = Paginator(meeting_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }

    return render(request, 'meetings/index.html', context)

def topic_meetings(request, slug):
    """
        Распределение по темам Нетворки
        slug - Слаг топика
    """

    # Получение нетворкингов по определенной теме
    topic = get_object_or_404(Topic, slug=slug)
    meeting_list = Meeting.objects.filter(topic=topic).order_by('-pub_date')[:10]

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

    # Получение цены нетворкинга
    price_meeting = f'{meeting.price} RUB'

    # Получение числа присутствующих
    presence_quantity = Presence.objects.filter(meeting=meeting).all().count()

    # Проверка аутификации пользователя
    if request.user.is_authenticated:

        # Проверяем Наличие подписки
        if (not Subscribe.objects.filter(user=request.user)) and (meeting.type == "ON") and (not Presence.objects.filter(user=request.user, meeting=meeting)):
            meeting.address = "*************"

        # Находим присутсвие его в нетворкингах
        presence = Presence.objects.filter(
            user=User.objects.get(username=request.user.username),
            meeting=meeting
        ).exists()

        if presence:
            price_meeting = "Уже Куплен"

    else:
        presence = None

        # Проверка, что Нетворк онлайн
        if meeting.type == "ON":
            meeting.address = "*************"


    context = {
        'meeting': meeting,
        'price_meeting': price_meeting,
        'presence': presence,
        'presence_quantity': presence_quantity,
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

    # Проверка Подписки у пользователя
    if Subscribe.objects.filter(user=request.user):
        # Получение Юзера
        user = get_object_or_404(User, username=request.user.username)

        # Получение Нетворкинга
        meeting = get_object_or_404(Meeting, pk=meeting_id)

        # Удаление Присутствия
        get_object_or_404(Presence, user=user, meeting=meeting).delete()

        # Удаление Ключа
        Key.objects.all().filter(user=user, meeting=meeting).delete()

        return redirect('customers:profile')

    else:
        return redirect('subscription:page_buy')

@login_required
def page_buy(request, meeting_id):
    """Страница Оплаты Нетворкинга"""

    # Получение нетворкинга
    meeting = get_object_or_404(Meeting, pk=meeting_id)

    # Создание label для оплаты подписки
    label_str = str(f'{request.user}{date.today()}{meeting.id}')

    # Создание ссылки для оплаты
    url_pay = payurl(meeting.price, label_str)

    context = {
        'base_url': url_pay,
        'sb_price': meeting.price,
        'product': meeting.title,
        'meeting': meeting,
        'meeting_id': meeting.id
    }

    return render(request, 'meetings/page_buy.html', context)

@login_required
def buy_check(request, meeting_id):
    """Проверка Оплаты"""

    # Получение нетворкинга
    meeting = get_object_or_404(Meeting, pk=meeting_id)

    # Создание label для оплаты нетворкинга
    label_str = str(f'{request.user}{date.today()}{meeting.id}')

    # Статус оплаты не завершен
    status = False

    # Подключение к PAY и проверки истории операций
    token = "4100118181285588.94A5D725FBD7058D703D55DEEA220ECBCCBB409846616298B7B09E8EA495BDCA7688A9EA11AEA351708FA57D54F854427C474264C4B373F9BDB27257D490CE67CAA17526DCC83EE9B019A46EB2DABA233C9C4264BC3F76362C4AC070994381964D28F70E648E4A9A5301EEBB98CA0AED3D8E53CA61AD02B203BEAFEEFE1A25C1"
    client = Client(token)
    history = client.operation_history(label=label_str)

    # Получение status
    for operation in history.operations:
        status = operation.status

    # Проверить status на получение оплаты
    if status:
        # Генерация Ключа
        key = str(random.randint(1000000000000000000000, 9999999999999999999999))
        link = "https://network-place.ru/profile/key-valid/" + key

        # Создание Ключа
        Key.objects.get_or_create(key=key, link=link, user=request.user, meeting=meeting)

        # Создание Присутствия
        Presence.objects.get_or_create(user=request.user, meeting=meeting)

        return redirect('customers:profile')

    # Получение url для повторной оплаты
    url_pay = payurl(meeting.price, label_str)

    context = {
        'base_url': url_pay,
        'status': status,
        'sb_price': meeting.price,
        'product': meeting.title,
        'meeting_id': meeting.id
    }

    return render(request, 'meetings/page_buy.html', context)
