from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model

from .forms import ContactForm, LoginForm, RegisterForm


def home_page_old(request):
    return HttpResponse("<h1>Hello world!</h1>")


def home_page(request):
    context = {
        "title": "Hello world!",
        "content": "Welcome to home page.",
        "premium_content": "YEAHHHHHHHH"
    }
    return render(request, 'home_page.html', context)


def about_page(request):
    context = {
        "title": "About us",
        "content": "Welcome to about page."
    }
    return render(request, 'home_page.html', context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title": "Contact us",
        "content": "Welcome to contact page.",
        "form": contact_form
    }

    if contact_form.is_valid():
        print(contact_form.cleaned_data)

    return render(request, 'contact_page.html', context)


def login_page(request):
    form = LoginForm(request.POST or None)
    print(request.user.is_authenticated)
    context = {
        'form': form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            # context['form'] = LoginForm()
            return redirect('/')

        else:
            # Return an 'invalid login' error message.
            print("Error in login")
    return render(request, "auth/login.html", context)


User = get_user_model()


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        new_user = User.objects.create_user(username, email, password)
    return render(request, "auth/register.html", context)
