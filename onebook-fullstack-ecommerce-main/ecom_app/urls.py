from django.urls import path

from ecom_app.views import Home_page_view
from ecom_app.views import Register_page_view
from ecom_app.views import Login_page_view
from ecom_app.views import Logout_page_view
from ecom_app.views import load_api_data
from ecom_app.views import Add_to_Cart
from ecom_app.views import AboutView
from ecom_app.views import detailed_view
from ecom_app.views import landingView
from ecom_app.views import Viewcart
from ecom_app.views import SellView
from ecom_app.views import BuyView



urlpatterns=[

    path("",landingView,name="landing"),
    path("home",Home_page_view,name="home"),
    path("register/",Register_page_view,name="register"),
    path("login/",Login_page_view,name="login"),
    path("logout/",Logout_page_view,name="logout"),
    
    path("load/",load_api_data,name="load"),
    path("cart/<int:product_id>",Add_to_Cart,name="add_to_cart"), # To add Products
    path("cart",Viewcart,name="viewcart"), # To View The Cat

    path("product/<int:product_id>",detailed_view,name="detailed_view"),
    path("about/",AboutView,name="about"),

    path("sell/",SellView,name="sell"), # To Sell / add item
    path("buy/",BuyView,name="buyNow"), 
 

    # comments
    # sell

]