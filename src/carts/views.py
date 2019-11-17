from django.shortcuts import render, redirect

# Create your views here.
from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail
from billing.models import BillingProfile
from orders.models import Order
from products.models import Product
from .models import Cart

# def cart_create(user=None):
#     """
#     Create a cart
#     """
#     cart_obj = Cart.objects.create(user=None)
#     print('create new cart')
#     return cart_obj


def cart_home(request):
    """
    """
    # print(request.session) # session was on the reqeust object by default
    # *** dir() could display the methods and attributes of an oject
    # print(dir(request.session))
    # *** let's try to get the session_key and print to console.
    # key = request.session.session_key
    # print(key)

    # *** let's try to set a key to session
    # *** we set the key here, and get the key from session in home page.
    # request.session['first_name'] = "Justin"
    # del request.session['cart_id']

    # cart_id = request.session.get("cart_id", None)
    # qs = Cart.objects.filter(id=cart_id)
    # if qs.count() == 1:
    #     print('Cart ID exists')
    #     cart_obj = qs.first()
    #     if request.user.is_authenticated and cart_obj.user is None:
    #         cart_obj.user = request.user
    #         cart_obj.save()
    # else:
    #     print(request.user)
    #     cart_obj = Cart.objects.new(user=request.user)
    #     request.session['cart_id'] = cart_obj.id

    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html", {"cart": cart_obj})


def cart_update(request):
    product_id = request.POST['product_id']
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Show message to user, product is gone?")
            return redirect("carts:home")
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    if product_obj in cart_obj.products.all():
        cart_obj.products.remove(product_obj)
    else:
        cart_obj.products.add(product_obj)
    request.session['cart_items'] = cart_obj.products.count()
    # return redirect(product_obj.get_absolute_url())
    return redirect("carts:home")


def checkout_home(request):
    cart_obj, new_created = Cart.objects.new_or_get(request)
    order_obj = None

    if new_created or cart_obj.products.count() == 0:
        return redirect("carts:home")

    user = request.user
    billing_profile = None
    login_form = LoginForm()
    guest_form = GuestForm()
    guest_email_id = request.session.get('guest_email_id')
    if user.is_authenticated:
        print('Here I am ', user)
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(
            user=user, email=user.email)
    elif guest_email_id is not None:
        guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
        billing_profile, billing_guest_profile_created = BillingProfile.objects.get_or_create(
            email=guest_email_obj.email)
    else:
        pass
    if billing_profile is not None:
        order_qs = Order.objects.filter(billing_profile=billing_profile, cart=cart_obj, active=True)
        if order_qs.count == 1:
            order_obj = order_qs.first()
        else:
            old_order_qs = Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj, active=True)
            if old_order_qs.exists():
                old_order_qs.update(active=False)
            order_obj = Order.objects.create(billing_profile=billing_profile, cart=cart_obj)

    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
    }

    return render(request, "carts/checkout.html", context)
