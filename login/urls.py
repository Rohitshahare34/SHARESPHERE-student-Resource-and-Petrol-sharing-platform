from django.urls import path
from .views import home_view, user_login  # Ensure correct import
from ridemate.views import submit_feedback  # Import submit_feedback view
from . import views

urlpatterns = [
    path("", user_login, name="login."),
    path('login/', user_login, name="login"),
    path("home/", home_view, name="home"), 
    path('submit-feedback/', submit_feedback, name="submit_feedback"),  # Updated URL pattern
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
]
