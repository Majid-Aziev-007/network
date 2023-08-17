from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Subscribe
from yoomoney import Quickpay, Client
from datetime import date

def payurl(sum, label):
    """
        Функция создание ссылки для оплаты
        sum - Сумма Платежа
        label - Лейбл к платежу для его уникальности
    """

    # Создаём ссылку с оплатой
    quickpay = Quickpay(
                receiver="4100118181285588",
                quickpay_form="shop",
                targets="Sponsor this project",
                paymentType="SB",
                sum=sum,
                label=label)

    # Отдаём ссылку с оплатой
    return quickpay.base_url

@login_required
def page_buy(request):
    """Страница Оплаты Подписки"""

    # Создание ссылки для оплаты
    url_pay = payurl(2, str(f'{request.user}{date.today()}'))

    context = {
        'base_url': url_pay
    }

    return render(request, 'subscription/page_buy.html', context)

@login_required
def buy_check(request):
    """Проверка Оплаты"""

    status = False

    # Подключение к PAY и проверки истории операций
    token = "4100118181285588.94A5D725FBD7058D703D55DEEA220ECBCCBB409846616298B7B09E8EA495BDCA7688A9EA11AEA351708FA57D54F854427C474264C4B373F9BDB27257D490CE67CAA17526DCC83EE9B019A46EB2DABA233C9C4264BC3F76362C4AC070994381964D28F70E648E4A9A5301EEBB98CA0AED3D8E53CA61AD02B203BEAFEEFE1A25C1"
    client = Client(token)
    history = client.operation_history(label=str(f'{request.user}{date.today()}'))

    # Получение status
    for operation in history.operations:
        status = operation.status

    # Проверить status на получение оплаты
    if status:
        Subscribe.objects.get_or_create(user=request.user)

        return redirect('customers:profile')

    # Получение url для повторной оплаты
    url_pay = payurl(2, str(f'{request.user}{date.today()}'))

    context = {
        'base_url': url_pay,
        'status': status
    }

    return render(request, 'subscription/page_buy.html', context)
