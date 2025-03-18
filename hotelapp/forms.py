from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Booking, Room 



User=get_user_model()
class UserSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15,required=True)
    

    class Meta:
        
        model =User
        fields = ["username", "email", "phone_number", "password1", "password2"]
          
# Login Form
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



class BookingForm(forms.ModelForm):
    
    class Meta:
        model = Booking
        fields = [ "check_in", "check_out", "guests"]
        widgets = {
            "check_in": forms.DateInput(attrs={"type": "date", "class": "form-control","id":"checkin"}),
            "check_out": forms.DateInput(attrs={"type": "date", "class": "form-control","id":"checkout"}),
            "guests": forms.NumberInput(attrs={"class": "form-control"}),
        }
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["room_type","price_per_night","total_rooms","image"]

class SearchRoomForm(forms.Form):
    
    check_in = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control',"id":"checkin"}))
    check_out = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control',"id":"checkout"}))
    guests = forms.IntegerField(min_value=1, max_value=5, required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))

         



