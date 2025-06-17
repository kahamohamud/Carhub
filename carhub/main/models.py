from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_dealer = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

class Dealer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='dealer_images/', blank=True, null=True)
    email = models.EmailField()

    def __str__(self):
        return self.user.username

class Car(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='car_images/')

    def __str__(self):
        return self.name

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.car.name}"
