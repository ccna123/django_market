from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings
from django.contrib.auth import get_user_model
import locale
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUser(AbstractUser):
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=1000)
    
    @property
    def budget_convert(self):
        locale.setlocale(locale.LC_ALL, '')
        return locale.currency(self.budget, grouping=True).replace(".00", "").replace("$", "")
    

class Item(models.Model):
    owner = models.ForeignKey('main.CustomUser' , default=None, blank=True, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    desc = models.CharField(max_length=1024)
    image_url = models.CharField(max_length=512)
    remain = models.IntegerField(default=0)
    size = models.CharField(max_length=255, blank=True)
    age = models.PositiveIntegerField(default=7)
    origin = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.name
    
    @property
    def get_price(self):
        return self.price
    
    @property
    def price_convert(self):
        locale.setlocale(locale.LC_ALL, '')
        return locale.currency(self.price, grouping=True).replace(".00", "").replace("$", "")

class Inventory(models.Model):
    
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True, null=True)
    bought_quantity = models.IntegerField(blank=True, default=0)
    rating_score = models.IntegerField(blank=True, default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comments = models.CharField(max_length=1024, blank=True, null=True)
    is_in_inventory = models.BooleanField(default=False)
    is_buying = models.BooleanField(default=False)
    
    
    def get_total(self):
        return self.quantity * self.item.price
    
    @property
    def total_convert(self):
        locale.setlocale(locale.LC_ALL, '')
        return locale.currency(self.get_total(), grouping=True).replace(".00", "").replace("$", "")
    
        
