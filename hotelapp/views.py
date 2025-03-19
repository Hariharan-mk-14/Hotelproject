from django.shortcuts import render,redirect,get_object_or_404
from .models import User, Room, Booking
from .forms import UserSignupForm,LoginForm,BookingForm,RoomForm,SearchRoomForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import random
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.utils.dateparse import parse_date
import stripe
from .models import Payment
from django.conf import settings
from django.urls import reverse

# Create your views here.
def home(request):
    return render(request,'home.html')
def signup(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save but don't commit yet
            user.set_password(form.cleaned_data["password1"])  # Hash password
            user.save()  # Now save the user into the database

            #login(request, user)  # Auto-login after signup
            messages.success(request, "Signup successful! Welcome.")
            return redirect("home")
        else:
            messages.error(request, "Signup failed. Please correct the errors.")
    else:
        form = UserSignupForm()
    
    return render(request, "signup.html", {"form": form})# Login View
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)

            if user is not None : 
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Invalid credentials .")
    else:
        form = LoginForm()
    
    return render(request, "userlogin.html", {"form": form})
@login_required
def user_profile(request):
    bookings=Booking.objects.filter(user_id=request.user.id).all()
    return render(request,"admindashboard.html",{'users':users,'bookings':bookings,'rooms':rooms})
def cancel_room(request):
    bookings=Booking.objects.filter(user_id=request.user.id).values_list("status",flat=True)
    if bookings=="Confirmed" :
        messages.success(request,"success")
    else:
        
        bookings.save(update_fields="status")
        messages.success(request,"your has accepted")
    return redirect('userprofile')   

def user_logout(request):
    logout(request)
    return redirect('home')
@login_required
def admin_dashboard(request):
    if not request.user.is_admin:
        return redirect('home')
    users = User.objects.all().order_by('-last_login')
    bookings= Booking.objects.all()
    rooms= Room.objects.all()
    return render(request,"admindashboard.html",{'users':users,'bookings':bookings,'rooms':rooms})
@login_required
def delete_user(request,user_id):
    if not request.user.is_admin:
        return redirect('admindashboard')
    user=User.objects.filter(id=user_id)
    if user!= request.user:
        user.delete()
        return redirect('admindashboard')

# @login_required
# def booking(request):
#     rooms = Room.objects.all()
#     booked_rooms = Booking.objects.filter().values_list("room_id", flat=True)
#     rooms = rooms.exclude(id__in=booked_rooms)
#     return render(request, "booking.html", { "rooms": rooms})
   
def rooms(request):
    form = SearchRoomForm()
    rooms = Room.objects.all()
    guests = request.GET.get("guests")
   
    if request.method == "GET":
        form = SearchRoomForm(request.GET)
        if form.is_valid():
            check_in = parse_date(request.GET.get("check_in"))
            check_out = parse_date(request.GET.get("check_out"))
            booked_rooms = Booking.objects.filter(check_in__lt=check_out, check_out__gt=check_in).values_list("room_id", flat=True)
            rooms = rooms.exclude(id__in=booked_rooms)
            if check_in<=check_out:
                if request.user.is_authenticated:
                    return render(request, "booking.html", { "rooms": rooms})
                else:
                    return redirect("userlogin")
            else:
                messages.error(request,"check out date should be equal or later to check in date.")
            
    return render(request, "rooms.html", {"form": form})

def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user=User.objects.filter(email=email).first()
        if user:
            otp = random.randint(100000, 999999)  # Generate OTP
            send_mail(
                'Password Reset OTP',
                f'Your OTP is: {otp}',
                'hariharamani2004@gmail.com',
                [email],

            )
            request.session['reset_otp'] = otp
            request.session['email'] = email
            return redirect('password_reset_verify')
        else:
            messages.error(request,"email not found, please enter registered email ")
    return render(request, "forgotpassword.html")
def password_reset_verify(request):
    if request.method == 'POST':
        entered_otp = int(request.POST.get('otp'))
        saved_otp = request.session.get('reset_otp')
        if entered_otp == saved_otp:
            return redirect('new_password_set')  # Or redirect to a password reset form
        else:
            messages.error(request,"wrong otp")
            return render(request, 'passwordresetverify.html', {'error': 'Invalid OTP'})
    return render(request, 'passwordresetverify.html')
def new_password_set(request):
    if request.method == 'POST':
        new_password= request.POST.get("new_password")
        confirm_password= request.POST.get('confirm_password')
        email=request.session.get('email')
        if new_password != confirm_password:
            messages.error(request,"password do not match!")
            return redirect("new_password_set")
        else:
            user=User.objects.filter(email=email).first()
            if user:
              
                user.set_password(new_password)
                user.save()
                messages.success(request,"password changed successfully")
                return redirect('userlogin')
            else:
                messages.error(request, "  error occured during password reset")
    return render(request, "passwordset.html")

# def hotel_list(request):
#     hotels = Hotel.objects.all()
#     return render(request, "hotel_list.html", {"hotels": hotels})

def available_rooms(request):
    # hotel = get_object_or_404(Hotel, id=hotel_id)
    
    rooms = Room.objects.all()
    # check_in = request.GET.get("check_in")
    # check_out = request.GET.get("check_out")
    # guests = request.GET.get("guests")

    # if check_in and check_out:
    #     check_in = parse_date(check_in)
    #     check_out = parse_date(check_out)
    booked_rooms = Booking.objects.filter(
         check_in__lt=check_out, check_out__gt=check_in
    ).values_list("room_id", flat=True)
    rooms = rooms.exclude(id__in=booked_rooms)

    return render(request, "booking.html", {"hotel": hotel, "rooms": rooms})

@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    date_list_in = list(Booking.objects.filter(room_id=room_id).values_list("check_in"))
    date_list_out = list(Booking.objects.filter(room_id=room_id).values_list("check_out"))
    dates_in = [date[0].strftime('%Y-%m-%d') for date in date_list_in]
    dates_out = [date[0].strftime('%Y-%m-%d') for date in date_list_out]
    # checkin=book.check_in
    # checkout=book.check_out
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
        
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            if booking.check_out != booking.check_in:
                booking.total_price = room.price_per_night * (booking.check_out - booking.check_in).days
            else:
                booking.total_price = room.price_per_night
            if booking.check_out>=booking.check_in:
                match=False
                for d in dates_in:
                    if str(booking.check_in) == d or str(booking.check_out) == d:
                        print("checkout",booking.check_out)
                        print(d)
                        match=True
                        break
                for d in dates_out:
                    if str(booking.check_out) == d or str(booking.check_in) ==d:
                        print("checkin",booking.check_in)
                        print(d)
                        match=True
                        break
                if match:
                    messages.error(request,"This room is not available on these dates!!")
                else:
                    booking.save()
                    return redirect(reverse('stripe_payment', args=[room_id]))    
            else:
                messages.error(request,"check out date should be same or later to check in date.")
            
    else:
        form = BookingForm()
    
    
    return render(request, "book_room.html", {"form": form, "room": room})

@login_required
def booking_success(request):
    return render(request, "booking_success.html")
def update_rooms(request):
    if request.user.is_admin:
        if request.method=='POST':
            form = RoomForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request,"Room Updated Successfully.")
                return redirect('admindashboard')
        else:
                form = RoomForm()
        return render(request,'update_rooms.html',{'form':form}) 
def cancel_room(request,room_id):
    book=Booking.objects.filter(room_id=room_id)
    book.delete()
    messages.success(request,"Room cancelled! ")
    return redirect("userprofile")

def stripe_payment(request ,room_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    bookroom = Booking.objects.filter(room_id=room_id).first()
    room=bookroom.room
    bookprice =Booking.objects.filter(room_id=room_id).first()
    price= int(bookprice.total_price*100)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
        'price_data': {
            'currency': 'INR',
            'product_data': {
                'name': room,
            },
            'unit_amount': price,
        },
        'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8000/paymentsuccess/',
        cancel_url='http://localhost:8000/paymentfailed/',
    )
    
    return render(request, 'stripe_payment.html', {'session_id': session.id,'price':price})


    
    
    # # if request.method == "POST":
    # #     amount = int(float(request.POST.get("amount")) * 100) # Convert to paisa
    # #     client = stripe.Client(auth=(settings.STRIPE_KEY_ID, settings.STRIPE_KEY_SECRET))
    # #     payment_data = client.order.create({"amount": amount, "currency": "INR", "payment_capture": 1})
    # #     payment = Payment.objects.create(user=request.user, amount=amount / 100, payment_id=payment_data["id"])
    # #     room=Room.objects.all()
    # #     return render(request, "stripe_payment.html", {"payment_data": payment_data, "stripe_key": settings.STRIPE_KEY_ID,"room":room})
    
    # return render(request, "stripe_payment.html")
def payment_success(request):
    return render(request,"payment_success.html")
def payment_failed(request):
    return render(request,"payment_failed.html")
def contact(request):
    return render(request,"contact.html")
