from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    is_admin = models.BooleanField(default = False)
    lastLogin = models.DateTimeField(null=True)
    cart_value = models.IntegerField(default=0)
    cart_item = models.JSONField(null = True,blank = True)
    order  = models.JSONField(null=True,blank = True)
    order_value = models.IntegerField(default = 0)
    auth_token = models.CharField(max_length=200,default = None,null = True)
    is_authenticated = models.BooleanField(default = False)



    def __str__(self):
        return f"{self.name}"
class item(models.Model):
    brand_name = models.CharField(max_length = 50)
    item_name = models.CharField(max_length=50)
    desc = models.CharField(max_length=200,blank=True)
    discounted_price = models.IntegerField()
    actual_price = models.IntegerField()
    available_number = models.IntegerField()
    image = models.ImageField(upload_to='images/', default='images/loading.png',max_length=100)
    

    def __str__(self):
        return f"{self.item_name} at {self.discounted_price} $"
    
class cart(models.Model):
    user = models.ForeignKey(User,on_delete =models.CASCADE)
    product = models.ManyToManyField(item)
    total_discounted_price = models.IntegerField(default = 0)

    def __str__(self):
        return f"{self.user} to pay {self.total_discounted_price}"
    
class wishlist(models.Model):
    user = models.ForeignKey(User,on_delete =models.CASCADE)
    product = models.ManyToManyField(item)

    def __str__(self):
        return f"{self.user} wishlisted item {self.product}"
    

    