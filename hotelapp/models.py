from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class User(AbstractUser):
    is_customer=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)


class Room(models.Model):
    
    room_type = models.CharField(max_length=50) # e.g., Deluxe, Suite
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    total_rooms = models.IntegerField()
    image= models.ImageField(upload_to='rooms/')
    

    def __str__(self):
        return f"  {self.room_type}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[("Confirmed", "Confirmed"), ("Cancelled", "Cancelled")], default="Confirmed")

    def __str__(self):
        return f"{self.user.username}  ({self.check_in} to {self.check_out})"


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - ₹{self.amount} - {'Paid' if self.is_paid else 'Pending'}"
