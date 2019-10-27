from django.shortcuts import render

# Create your views here.

def cart_home(request):
    print(request.session) # session was on the reqeust object by default
    # *** dir() could display the methods and attributes of an oject
    # print(dir(request.session))
    # *** let's try to get the session_key and print to console.
    # key = request.session.session_key
    # print(key)

    # *** let's try to set a key to session
    # *** we set the key here, and get the key from session in home page.
    request.session['first_name'] = "Justin"

    return render(request, "carts/home.html", {})