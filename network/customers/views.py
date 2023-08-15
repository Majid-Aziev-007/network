from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Key
from .forms import KeyForm

@login_required
def profile(request):

    keys = Key.objects.filter(user=request.user)

    paginator = Paginator(keys, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'link': 'https://network-place.ru/profile/key-valid/'
    }

    return render(request, 'customers/profile.html', context)


@login_required
def key_valid(request, key_input = None):
    if key_input:
        key = Key.objects.filter(key=key_input).first()

        if key:
            context = {
                'answer': 'Ключ Действителен',
            }
                
        else:
            context = {
                'answer': 'Ключ Не Действителен',
            }

        return render(request, 'customers/key.html', context)  
    
    if request.user.get_group_permissions():
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
                    }
                
                else:
                    context = {
                        'form': form,
                        'answer': 'Ключ Не Действителен',
                    }

                return render(request, 'customers/key.html', context)          

            return render(request, 'customers/key.html', {'form': form})  

        context = {
            'form': form,
        }

        return render(request, 'customers/key.html', context)            
    
    return render(request, 'meetings/index.html', context)
