from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Key
from .forms import KeyForm
from datetime import timedelta
from panelcreator.models import Creator

@login_required
def profile(request):
    """
        Профайл юзера
    """

    keys = Key.objects.filter(user=request.user)

    paginator = Paginator(keys, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'link': 'https://network-place.ru/profile/key-valid/',
    }

    return render(request, 'customers/profile.html', context)


@login_required
def key_valid(request, key_input = None):
    """
        Проверка Ключа пользователя к Нетворкингу
        key_input - Ввод ключа
    """

    creator = Creator.objects.filter(user=request.user).exists()

    if creator:

        # Если key_input передан
        if key_input:
            # Находим ключ
            key = Key.objects.filter(key=key_input).first()

            # Проверка существования ключа
            if key:
                context = {
                    'answer': 'Ключ Действителен',
                    'key': key
                }
                    
            else:
                context = {
                    'answer': 'Ключ Не Действителен',
                }

            return render(request, 'customers/key.html', context)  
    
        form = KeyForm(request.POST)
        if request.method=='POST':
            if form.is_valid():
                cd = form.cleaned_data
                key_input = cd.get('key_input')
                key = Key.objects.filter(key=key_input).first()

                if key:
                    context = {
                        'form': form,
                        'answer': 'Ключ Действителен',
                        'key': key
                    }
                
                else:
                    context = {
                        'form': form,
                        'answer': 'Ключ Не Действителен',
                        'key': key
                    }

                return render(request, 'customers/key.html', context)          

            return render(request, 'customers/key.html', {'form': form})  

        context = {
            'form': form,
        }

        return render(request, 'customers/key.html', context)            
    
    return render(request, 'meetings/index.html', context)
