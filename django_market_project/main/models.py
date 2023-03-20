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

    shop_link = models.CharField(max_length=512, blank=True)
    name = models.CharField(max_length=255)
    image_url = models.CharField(max_length=512)
    instruction = models.CharField(max_length=2048, blank=True)
    
    def __str__(self):
        return self.name
    

class Inventory(models.Model):
    
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    rating_score = models.IntegerField(blank=True, default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comments = models.CharField(max_length=1024, blank=True, null=True)
    is_in_inventory = models.BooleanField(default=False)
    
        
