from django.urls import path
from .views import (
    ridemate_home, offer_ride, submit_feedback, ridemate_profile, 
    edit_ridemate_profile, update_preferences, rate_ride, edit_ride, 
    cancel_ride, cancel_booking, ride_requests, handle_request
)

urlpatterns = [
    path('', ridemate_home, name='ridemate_home'),  # Ensure this name matches the URL used in home.html
    path('offer-ride/', offer_ride, name='offer_ride'),
    path('find-ride/', ridemate_home, name='find_ride'),  # Using ridemate_home view for now
    path('guidelines/', ridemate_home, name='guidelines'),  # Using ridemate_home view for now
    path('student-feedback/', submit_feedback, name='student_feedback'),
    path('submit-feedback/', submit_feedback, name='submit_feedback'),
    path('profile/', ridemate_profile, name='ridemate_profile'),
    path('profile/edit/', edit_ridemate_profile, name='edit_ridemate_profile'),
    path('profile/preferences/', update_preferences, name='update_preferences'),
    path('ride/<int:ride_id>/edit/', edit_ride, name='edit_ride'),
    path('ride/<int:ride_id>/cancel/', cancel_ride, name='cancel_ride'),
    path('booking/<int:request_id>/cancel/', cancel_booking, name='cancel_booking'),
    path('ride/<int:ride_id>/requests/', ride_requests, name='ride_requests'),
    path('request/<int:request_id>/<str:action>/', handle_request, name='handle_request'),
    path('rate/<int:ride_id>/', rate_ride, name='rate_ride'),
]
