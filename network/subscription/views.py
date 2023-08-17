from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Subscribe
from yoomoney import Quickpay
from yoomoney import Client
from datetime import date

@login_required
def page_buy(request):

    quickpay = Quickpay(
                receiver="4100118181285588",
                quickpay_form="shop",
                targets="Sponsor this project",
                paymentType="SB",
                sum=2,
                label=str(f'{request.user}{date.today()}')
                )

    context = {
        'base_url': quickpay.base_url
    }

    return render(request, 'subscription/page_buy.html', context)

@login_required
def buy_check(request):

    token = "4100118181285588.94A5D725FBD7058D703D55DEEA220ECBCCBB409846616298B7B09E8EA495BDCA7688A9EA11AEA351708FA57D54F854427C474264C4B373F9BDB27257D490CE67CAA17526DCC83EE9B019A46EB2DABA233C9C4264BC3F76362C4AC070994381964D28F70E648E4A9A5301EEBB98CA0AED3D8E53CA61AD02B203BEAFEEFE1A25C1"
    client = Client(token)
    history = client.operation_history(label=str(f'{request.user}{date.today()}'))
    status = "Оплаты Нет"

    for operation in history.operations:
        status = operation.status
        print(status)

    quickpay = Quickpay(
                receiver="4100118181285588",
                quickpay_form="shop",
                targets="Sponsor this project",
                paymentType="SB",
                sum=10,
                label=str(f'{request.user}{date.today()}')
                )

    context = {
        'base_url': quickpay.base_url,
        'status': status
    }

    if status == "success":
        Subscribe.objects.get_or_create(user=request.user)

        return redirect('customers:profile')

    return render(request, 'subscription/page_buy.html', context)
