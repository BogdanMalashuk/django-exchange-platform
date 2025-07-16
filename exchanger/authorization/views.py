from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.http import require_POST


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
            return redirect('ad_list')
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect('ad_list')
