from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model

from .forms import ContactForm


def home_page_old(request):
    return HttpResponse("<h1>Hello world!</h1>")


def home_page(request):
    # *** get the data from session, the data was set from cart view.
    # first_name = request.session.get('first_name')
    # print(first_name)
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
        "form": contact_form,
        "brand": "new Brand Name"
    }

    if contact_form.is_valid():
        print(contact_form.cleaned_data)

    return render(request, 'contact_page.html', context)    