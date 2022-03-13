from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_police = models.BooleanField(default=False)
    is_repair = models.BooleanField(default=False)
    is_insurance = models.BooleanField(default=False)
    is_shop = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
class Product (models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name

class Insurance (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.TextField()
    is_claimed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Repair (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Theft (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.TextField()
    is_solved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username