from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
# from ecom_app.forms import Registration_form
from django.contrib.auth.forms import UserCreationForm as Registration_form

from django.contrib.auth.forms import AuthenticationForm as Login_form
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

import requests

import random

from ecom_app.models import Product_Model
from ecom_app.models import Cart_Model
from ecom_app.models import Cart_item

def landingView(req):

    return render(req,"landing.html")

@login_required(login_url="login")
def Home_page_view(req):

        all_data=Product_Model.objects.all()

        context={
            "all_data":all_data,
            "username": req.user.username,
        }

        return render(req,"home.html", context)
    
    
def Login_page_view(req):

    if req.method=="POST":

        data=Login_form(data=req.POST)

        if data.is_valid():
            login(req,data.get_user())
            return redirect("home")
        else:
            error_message = "Invalid data. Please check your input."
                
            return render(req, "error.html", context={"error": error_message})

    context={
        "form" : Login_form,
        "username": req.user.username,
    }
    
    return render(req,"login.html",context)
    
def Logout_page_view(req):

    logout(req)
    
    return redirect("landing")


def Register_page_view(req):

    if req.method=="POST":
        
        new_user=Registration_form(req.POST)
        
        if new_user.is_valid():
            login(req,new_user.save())
            return redirect("home")
        else:
            if 'username' in new_user.errors and 'unique' in new_user.errors['username']:
                error_message = "Username is already taken. Please choose a different one."
            else:
                error_message = "Invalid data. Please check your input.\nUsername Might already be taken try Different One"

            return render(req, "error.html", context={"error": error_message})
    else:
        context={
            "Registration_form" : Registration_form
        }

        return render(req,"register.html",context)

def load_api_data(req):

    # api_data=requests.get("https://fakestoreapi.com/products")
    api_data=requests.get("https://www.dbooks.org/api/recent")

    if api_data.status_code==200:

        json_data=api_data.json()
        json_data=json_data["books"]

        for item in json_data:
            title=item.get("title")
            price=random.randint(100,999)
            author=item.get("authors")
            subtitle=item.get("subtitle")
            image=item.get("image")
            url=item.get("url")

            Product_Model.objects.create(
                title=title,
                price=price,
                author=author,
                subtitle=subtitle,
                url=url,
                image=image,
            )

        return redirect("home")
    else:
        return HttpResponse("Failed to Fetch Data :( ")


# Short Summary how we are adding products into the cart
"""
You retrieve the product instance based on the provided product ID. Then, you check if a user is logged in. If a user is logged in, you retrieve the corresponding user instance. After that, you create or retrieve the cart associated with the user. If the cart doesn't exist, it's created. Next, you add the retrieved product to the cart. Finally, you render the cart page with the updated list of products in the cart (Frontend).
"""
# =======================================

@login_required(login_url="login")
def Add_to_Cart(req, product_id):
    if req.user.is_authenticated:
        product_to_add = get_object_or_404(Product_Model, id=product_id)
        item_in_cart, already_exist = Cart_item.objects.get_or_create(products=product_to_add)
        if already_exist:
            item_in_cart.quantity += 1
            item_in_cart.save() 

        cart_instance, _ = Cart_Model.objects.get_or_create(user=req.user)
        cart_instance.items.add(item_in_cart)

        total_money = cart_instance.total_price() if hasattr(cart_instance, 'total_price') else None

        context = {
            "total": total_money,
            "product_in_cart": cart_instance.items.all(),
            "username": req.user.username,
        }
        return render(req, "cart_v_2.html", context)
    else:
        return redirect("login")

# ====================================================
@login_required(login_url="login")
def Viewcart(req):

    cart_instance, already_exist = Cart_Model.objects.get_or_create(user=req.user)

    product_in_cart=cart_instance.items.all()
    context={
        "product_in_cart":product_in_cart,
        "user_id": User.id,
        "username": req.user.username,
    }

    return render(req,"cart_v_2.html",context)

@login_required(login_url="login")
def AboutView(req):
    context={
        "user_id":User.id,
        "username": req.user.username,
    }
    return render(req,"about.html",context)

@login_required(login_url="login")
def detailed_view(req,product_id):

    this_product_data=Product_Model.objects.get(id=product_id)

    context={
        "user_id":req.user.id,
        "username":req.user.username,
        "this_product_data" : this_product_data

    }
    return render(req,"detailed_html.html",context)


#To add New Products
def SellView(req):
    pass

import random
import string
from django.utils import timezone

def BuyView(req):
    try:
        userCart = Cart_Model.objects.get(user=req.user)
        total = userCart.total_price()
        userCart.delete()
    except Cart_Model.DoesNotExist:
        total = 0

    amount = total if total else 0

    # Generate a unique order ID
    current_datetime = str(timezone.now())
    orderID = ''.join(random.choices(string.ascii_letters + string.digits + current_datetime, k=8))

    context = {
        "amount": amount,
        "orderID": orderID
    }
    return render(req, "buy.html", context)
