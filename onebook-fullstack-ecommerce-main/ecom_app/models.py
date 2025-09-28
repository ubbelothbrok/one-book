from django.db import models
from django.contrib.auth.models import User
gender_list=[
    ("male","Male"),
    ("female","Female"),
    ("others","others"),
]


class Product_Model(models.Model):
    title=models.CharField(max_length=500)
    author=models.CharField(max_length=500)
    subtitle=models.CharField(max_length=500)
    url=models.CharField(max_length=500)
    price=models.FloatField()
    image=models.TextField()

    def __str__(self):
        return self.title
    

class Cart_item(models.Model):

    products=models.ForeignKey(Product_Model,on_delete=models.CASCADE,db_constraint=False)
    quantity=models.PositiveIntegerField(default=0)

    def sub_total(self):
        return self.products.price * self.quantity


class Cart_Model(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,db_constraint=False)
    created_at = models.DateTimeField(auto_now_add=True)
    items=models.ManyToManyField(Cart_item)

    def total_price(self):
        
        total = 0
        for item in self.items.all():
            total += item.sub_total()
        return total

    def __str__(self):
        return f"Cart : {self.id} - User: {self.user.username}"
    

"""

one user can have one Cart Instance but that instance can have May products  Items 
Product: Represents individual products available for purchase.
CartItem: Represents items added to the cart, including information like quantity.
Cart: Represents the shopping cart, which can contain multiple CartItem instances.

"""