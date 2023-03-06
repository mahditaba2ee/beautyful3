from django.db import models
from Accounts.models import User
from Category.models import ProductModel 
# Create your models here.

class CoponModel(models.Model):
    copon_code = models.CharField(max_length=20)
    persen = models.PositiveIntegerField(null=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    users = models.ManyToManyField(User)



class OrderModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='order_to_user',null=True,blank=True)
    user_view=models.ForeignKey(User,on_delete=models.CASCADE,related_name='orderview_to_user',null=True,blank=True)
    name = models.CharField(max_length=50,null=True)
    email = models.CharField(max_length=100,null=True)
    address = models.CharField(max_length=500,blank=True)
    phone = models.CharField(max_length=13,blank=True)
    ostan = models.CharField(max_length=20,null=True)
    city = models.CharField(max_length=20,null=True)
    codepsty = models.CharField(max_length=11,null=True)
    view = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    price_all = models.PositiveIntegerField(null=True)
    price_off = models.PositiveIntegerField(null=True)
    price_with_post = models.PositiveBigIntegerField(null=True)
    pay_type = models.CharField(max_length=50,null=True)
    def total_price(self):
        return sum(item.get_cost() for item in self.orderitem_to_order.all())
    class Meta:
        ordering =('view',)

class OrderItemsModel(models.Model):
    order = models.ForeignKey(OrderModel,models.CASCADE,related_name='orderitem_to_order')
    product = models.ForeignKey(ProductModel,models.CASCADE,related_name='orderitem_to_product')
    price = models.IntegerField()
    number = models.IntegerField(default=1)
    view = models.BooleanField(default=False)

    def get_cost(self):
        return int(self.number) * int(self.price)

