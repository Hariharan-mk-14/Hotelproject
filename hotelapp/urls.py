from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name="home"),
    path('signup/',views.signup,name="signup"),
    path('login/',views.user_login,name="userlogin"),
    path('logout/',views.user_logout,name='logout'),
    path('userprofile/',views.user_profile,name='userprofile'),
    path('admindashboard/',views.admin_dashboard,name="admindashboard"),
    path('admindashboard/userdelete/<int:user_id>/',views.delete_user,name='delete_user'),
    # path('booking/',views.booking,name="booking"),
    path('rooms/',views.rooms,name="rooms"),
    path('password-reset-request/',views.password_reset,name="password_reset"),
    path('password-reset-verify/',views.password_reset_verify,name="password_reset_verify"),
    path('new-password-set/',views.new_password_set,name="new_password_set"),
    path("book/<int:room_id>/", views.book_room, name="book_room"),
    path("booking-success/", views.booking_success, name="booking_success"),
    path("update-room/", views.update_rooms,name="update_rooms"),
    path("cancel/<int:room_id>",views.cancel_room,name="cancel"),
    path("stripe/<int:room_id>/", views.stripe_payment, name="stripe_payment"),
    path("paymentsuccess/",views.payment_success,name="payment_success"),
    path("paymentfailed/",views.payment_failed,name="payment_failed"),
    path("contact/",views.contact,name="contact"),
   


]


   