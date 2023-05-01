from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Customer


def user_login(request):
    if request.user.is_authenticated:
        return redirect('store:home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('store:home')
        else:
            messages.error(request, 'User or password is invalid!!!')
            return redirect('user_login')
    return render(request, 'accounts/signin.html', {})


def user_register(request):
    if request.user.is_authenticated:
        return redirect('store:home')

    if request.method == 'POST':
        forms = SignUpForm(request.POST)

        if forms.is_valid():
            user = forms.save()
            first_name = forms.cleaned_data.get('first_name')
            last_name = forms.cleaned_data.get('last_name')
            email = forms.cleaned_data.get('email')
            is_male = bool(int(request.POST['is_male']))
            customer = Customer.objects.create(first_name=first_name, last_name=last_name, email=email, user=user, is_male=is_male)
            customer.save()
            return redirect('user_login')
        else:
            messages.error(request, 'User already exist!!!')
            return redirect('user_register')
    else:
        forms = SignUpForm()
    return render(request, 'accounts/register.html', {'forms': forms})


def user_logout(request):
    logout(request)
    return redirect('user_login')
