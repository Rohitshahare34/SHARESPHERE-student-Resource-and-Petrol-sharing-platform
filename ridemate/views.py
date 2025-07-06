# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.utils.timezone import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings

# Python standard library imports
from datetime import datetime, timedelta

# Local imports
from .models import (
    Ride, 
    Testimonial, 
    RideRequest, 
    RidePreferences, 
    RideFeedback, 
    RideMateProfile
)
from login.models import Users

# Create your views here.
def update_expired_rides():
    """Update the is_expired status of rides based on their expiry time."""
    current_time = timezone.now()
    # Update rides where expiry_time has passed and is_expired is False
    Ride.objects.filter(
        expiry_time__lte=current_time,
        is_expired=False
    ).update(is_expired=True)

def ridemate_home(request):
    if "user_usn" not in request.session:
        return redirect('login')
    
    # Update expired rides
    update_expired_rides()
    
    # Get current time
    current_time = timezone.now()
    
    # Get active rides only (not expired and not fully booked)
    rides = Ride.objects.filter(
        is_expired=False,
        is_booked=False,
        expiry_time__gt=current_time
    ).order_by('-created_at')
    
    # Get approved testimonials
    testimonials = Testimonial.objects.filter(is_approved=True).order_by('-created_at')
    
    # Get today's date for form validation
    today = timezone.now().date()
    
    context = {
        'rides': rides,
        'testimonials': testimonials,
        'today': today,
        'user_usn': request.session.get('user_usn'),
    }
    return render(request, 'ridemate_home.html', context)

def offer_ride(request):
    if "user_usn" not in request.session:
        return JsonResponse({'success': False, 'message': 'Please login first'})
    
    if request.method == "POST":
        try:
            # Get the logged-in user
            user_usn = request.session.get("user_usn")
            try:
                user = Users.objects.get(usn=user_usn)
            except Users.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'User not found'})

            # Get form data
            name = request.POST.get("name")
            destination = request.POST.get("destination")
            seats = request.POST.get("seats")
            contact = request.POST.get("contact")
            pickup_location = request.POST.get("pickup_location")
            vehicle_number = request.POST.get("vehicle_number")
            ride_date = request.POST.get("ride_date")
            ride_time = request.POST.get("ride_time")
            additional_notes = request.POST.get("additional_notes", "")
            expiry_hours_str = request.POST.get("expiry_hours", "2")
            
            # Get price per seat (default to 0 if not provided)
            price_per_seat = request.POST.get("price_per_seat", "0")
            try:
                price_per_seat = float(price_per_seat)
            except ValueError:
                price_per_seat = 0.0
                
            # Get gender preference (default to 'any' if not provided)
            gender_preference = request.POST.get("gender_preference", "any")

            # Validate required fields
            if not all([name, destination, seats, contact, pickup_location, 
                       vehicle_number, ride_date, ride_time]):
                return JsonResponse({
                    'success': False,
                    'message': 'All required fields must be filled out'
                })

            try:
                # Create datetime object for ride time
                ride_datetime_str = f"{ride_date} {ride_time}"
                ride_datetime = timezone.make_aware(
                    datetime.strptime(ride_datetime_str, "%Y-%m-%d %H:%M")
                )

                # Get expiry hours from form - convert to float to handle decimal values
                try:
                    # Check if the value is one of the quick expiry times (15, 30, 45 minutes)
                    if expiry_hours_str in ["15", "30", "45"]:
                        # Convert minutes to hours
                        expiry_hours = float(expiry_hours_str) / 60
                    else:
                        # Parse as decimal hours
                        expiry_hours = float(expiry_hours_str)
                except ValueError:
                    # Default to 2 hours if parsing fails
                    expiry_hours = 2.0
                
                # Calculate hours and minutes
                expiry_hours_int = int(expiry_hours)
                expiry_minutes = int((expiry_hours - expiry_hours_int) * 60)
                
                # Calculate expiry time
                expiry_time = timezone.now() + timedelta(hours=expiry_hours_int, minutes=expiry_minutes)

                # Check for duplicate rides within a short time window
                time_threshold = timezone.now() - timedelta(minutes=1)
                existing_ride = Ride.objects.filter(
                    usn=user,
                    destination=destination,
                    pickup_location=pickup_location,
                    ride_datetime=ride_datetime,
                    created_at__gte=time_threshold
                ).exists()

                if existing_ride:
                    return JsonResponse({
                        'success': False,
                        'message': 'A similar ride was just posted. Please wait a moment before posting again.'
                    })

                # Create new ride
                ride = Ride.objects.create(
                    usn=user,
                    name=name,
                    destination=destination,
                    seats_available=int(seats),
                    contact_number=contact,
                    pickup_location=pickup_location,
                    vehicle_number=vehicle_number,
                    additional_notes=additional_notes,
                    ride_datetime=ride_datetime,
                    expiry_time=expiry_time,
                    gender_preference=gender_preference,
                    is_booked=False,
                    is_expired=False,
                    price_per_seat=price_per_seat
                )

                return JsonResponse({
                    'success': True,
                    'message': 'Ride posted successfully!'
                })

            except ValueError as e:
                return JsonResponse({
                    'success': False,
                    'message': f'Invalid date/time format: {str(e)}'
                })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'An error occurred while posting your ride. Please try again.'
            })

    # If it's a GET request, show the offer ride form
    return render(request, 'ridemate_offer_ride.html')

@csrf_exempt
def submit_feedback(request):
    if request.method == 'POST':
        try:
            # Get form data
            name = request.POST.get('name')
            department = request.POST.get('department')
            year = request.POST.get('year')
            feedback_text = request.POST.get('feedback_text')
            
            # Print debug information
            print(f"Received feedback data: name={name}, department={department}, year={year}, feedback_text={feedback_text}")
            
            # Validate data
            if not all([name, department, year, feedback_text]):
                print("Validation failed: Missing required fields")
                return JsonResponse({
                    'success': False,
                    'message': 'All fields are required'
                })
            
            try:
                # Create new testimonial
                testimonial = Testimonial.objects.create(
                    name=name,
                    department=department,
                    year=year,
                    feedback_text=feedback_text,
                    is_approved=True  # Auto-approve for demo purposes
                )
                print(f"Created testimonial with ID: {testimonial.id}")
                
                return JsonResponse({
                    'success': True,
                    'message': 'Feedback submitted successfully'
                })
            except Exception as e:
                print(f"Error creating testimonial: {str(e)}")
                return JsonResponse({
                    'success': False,
                    'message': f'Error saving feedback: {str(e)}'
                })
                
        except Exception as e:
            print(f"Error processing feedback: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })

@login_required
def ridemate_profile(request):
    """
    View the RideMate profile of the logged-in user.
    Creates a profile if one doesn't exist yet.
    """
    # Get or create the user's RideMate profile
    profile, created = RideMateProfile.objects.get_or_create(user=request.user)
    
    # Get rides offered by this user
    user_rides = Ride.objects.filter(usn=request.user, expiry_time__gt=timezone.now()).order_by('-ride_datetime')
    
    # Get rides booked by this user
    booked_rides = RideRequest.objects.filter(
        requestor=request.user, 
        ride__expiry_time__gt=timezone.now(),
        status="Accepted"
    ).select_related('ride', 'ride__usn').order_by('ride__date', 'ride__time')
    
    # Format booked rides for display
    formatted_booked_rides = []
    for request in booked_rides:
        ride_info = {
            'id': request.id,
            'pickup_location': request.ride.pickup_location,
            'destination': request.ride.destination,
            'date': request.ride.date,
            'time': request.ride.time,
            'price': request.ride.price,
            'vehicle_type': request.ride.vehicle_type,
            'driver': request.ride.usn,
            'request_status': request.status
        }
        formatted_booked_rides.append(ride_info)
    
    # Get past rides (both offered and taken)
    past_offered = Ride.objects.filter(usn=request.user, expiry_time__lte=timezone.now()).order_by('-date', '-time')
    past_taken_requests = RideRequest.objects.filter(
        requestor=request.user, 
        ride__expiry_time__lte=timezone.now(),
        status="Accepted"
    ).select_related('ride', 'ride__usn').order_by('-ride__date', '-ride__time')
    
    # Format past rides for display
    past_rides = []
    
    # Add past offered rides
    for ride in past_offered:
        # Get accepted requests for this ride
        passengers = RideRequest.objects.filter(ride=ride, status="Accepted")
        
        for passenger in passengers:
            # Create an entry for each passenger interaction
            ride_info = {
                'id': ride.id,
                'pickup_location': ride.pickup_location,
                'destination': ride.destination,
                'date': ride.date,
                'time': ride.time,
                'price': ride.price,
                'vehicle_type': ride.vehicle_type,
                'is_driver': True,
                'other_user': passenger.requestor,
                'rating': passenger.rider_rating
            }
            past_rides.append(ride_info)
    
    # Add past taken rides
    for request in past_taken_requests:
        ride_info = {
            'id': request.id,
            'pickup_location': request.ride.pickup_location,
            'destination': request.ride.destination,
            'date': request.ride.date,
            'time': request.ride.time,
            'price': request.ride.price,
            'vehicle_type': request.ride.vehicle_type,
            'is_driver': False,
            'other_user': request.ride.usn,
            'rating': request.driver_rating
        }
        past_rides.append(ride_info)
    
    # Sort past rides by date and time (most recent first)
    past_rides.sort(key=lambda x: (x['date'], x['time']), reverse=True)
    
    # Get user ride statistics
    rides_offered_count = Ride.objects.filter(usn=request.user).count()
    rides_taken_count = RideRequest.objects.filter(requestor=request.user, status="Accepted").count()
    
    # Calculate user rating
    driver_ratings = RideRequest.objects.filter(ride__usn=request.user, driver_rating__isnull=False).values_list('driver_rating', flat=True)
    rider_ratings = RideRequest.objects.filter(requestor=request.user, rider_rating__isnull=False).values_list('rider_rating', flat=True)
    
    all_ratings = list(driver_ratings) + list(rider_ratings)
    rating = round(sum(all_ratings) / len(all_ratings), 1) if all_ratings else 'N/A'
    
    # Get user preferences
    try:
        preferences = RidePreferences.objects.get(user=request.user)
    except RidePreferences.DoesNotExist:
        preferences = None
    
    context = {
        'profile': profile,
        'user_rides': user_rides,
        'booked_rides': formatted_booked_rides,
        'past_rides': past_rides,
        'rides_offered': rides_offered_count,
        'rides_taken': rides_taken_count,
        'rating': rating,
        'preferences': preferences,
        'created': created
    }
    
    return render(request, 'ridemate_profile.html', context)

@login_required
def edit_ridemate_profile(request):
    """
    Edit the RideMate profile of the logged-in user.
    """
    # Get or create the user's RideMate profile
    profile, created = RideMateProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Update profile information from form
        profile.bio = request.POST.get('bio', '')
        profile.preferred_pickup_locations = request.POST.get('preferred_pickup_locations', '')
        profile.preferred_destinations = request.POST.get('preferred_destinations', '')
        profile.vehicle_number = request.POST.get('vehicle_number', '')
        profile.vehicle_type = request.POST.get('vehicle_type', '')
        profile.phone_number = request.POST.get('phone_number', '')
        profile.is_driver = request.POST.get('is_driver', '') == 'on'
        
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        
        profile.save()
        
        # Update User model fields
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('ridemate_profile')
    
    context = {
        'profile': profile
    }
    
    return render(request, 'edit_ridemate_profile.html', context)

def update_preferences(request):
    """View for updating the user's ride preferences."""
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        user = request.user
        
        # Get form data
        common_destinations = request.POST.get('common_destinations', '')
        preferred_morning = request.POST.get('preferred_morning', '')
        preferred_evening = request.POST.get('preferred_evening', '')
        vehicle_model = request.POST.get('vehicle_model', '')
        vehicle_number = request.POST.get('vehicle_number', '')
        
        # Get checkbox values
        music_allowed = 'music_allowed' in request.POST
        smoking_allowed = 'smoking_allowed' in request.POST
        pets_allowed = 'pets_allowed' in request.POST
        
        # Update or create preferences
        preferences, created = RidePreferences.objects.get_or_create(user=user)
        
        preferences.common_destinations = common_destinations
        preferences.preferred_morning = preferred_morning
        preferences.preferred_evening = preferred_evening
        preferences.vehicle_model = vehicle_model
        preferences.vehicle_number = vehicle_number
        preferences.music_allowed = music_allowed
        preferences.smoking_allowed = smoking_allowed
        preferences.pets_allowed = pets_allowed
        
        preferences.save()
        
        # Redirect to profile page
        return redirect('ridemate_profile')
    
    # If not POST, redirect to profile
    return redirect('ridemate_profile')

def rate_ride(request, ride_id):
    """View for rating a completed ride."""
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        
        try:
            # Determine if this is a ride request or a ride
            try:
                # First check if it's a ride request ID
                ride_request = RideRequest.objects.get(id=ride_id)
                
                # User is rating the driver
                ride_request.driver_rating = rating
                ride_request.driver_comment = comment
                ride_request.save()
                
            except RideRequest.DoesNotExist:
                # Check if it's a ride ID and find the corresponding request
                ride = Ride.objects.get(id=ride_id)
                
                # Make sure user is the ride creator
                if ride.usn != request.user:
                    messages.error(request, "You are not authorized to rate this ride.")
                    return redirect('ridemate_profile')
                
                # Find the corresponding request to update
                passenger_id = request.POST.get('passenger_id')
                if passenger_id:
                    request_to_rate = RideRequest.objects.get(id=passenger_id, ride=ride)
                    request_to_rate.rider_rating = rating
                    request_to_rate.rider_comment = comment
                    request_to_rate.save()
                else:
                    messages.error(request, "Passenger information missing.")
            
            messages.success(request, "Your rating has been submitted successfully.")
            
        except (Ride.DoesNotExist, RideRequest.DoesNotExist, ValueError):
            messages.error(request, "Invalid ride information. Please try again.")
    
    return redirect('ridemate_profile')

def edit_ride(request, ride_id):
    """View for editing a ride offer."""
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        ride = Ride.objects.get(id=ride_id, usn=request.user)
    except Ride.DoesNotExist:
        messages.error(request, "Ride not found or you are not authorized to edit it.")
        return redirect('ridemate_profile')
    
    if request.method == 'POST':
        # Get form data
        pickup_location = request.POST.get('pickup_location')
        destination = request.POST.get('destination')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        price = request.POST.get('price')
        available_seats = request.POST.get('available_seats')
        vehicle_type = request.POST.get('vehicle_type')
        notes = request.POST.get('notes', '')
        
        # Validate data
        if not all([pickup_location, destination, date_str, time_str, price, available_seats]):
            messages.error(request, "All fields are required.")
            return render(request, 'edit_ride.html', {'ride': ride})
        
        # Update ride information
        ride.pickup_location = pickup_location
        ride.destination = destination
        ride.date = datetime.strptime(date_str, '%Y-%m-%d').date()
        ride.time = time_str
        ride.price = price
        ride.available_seats = available_seats
        ride.vehicle_type = vehicle_type
        ride.notes = notes
        
        # Calculate expiry time (end of the ride day)
        ride_datetime = datetime.combine(ride.date, datetime.strptime(time_str, '%H:%M').time())
        ride.expiry_time = ride_datetime.replace(hour=23, minute=59, second=59)
        
        ride.save()
        
        messages.success(request, "Ride updated successfully.")
        return redirect('ridemate_profile')
    
    context = {
        'ride': ride
    }
    
    return render(request, 'edit_ride.html', context)

def cancel_ride(request, ride_id):
    """View for cancelling a ride offer."""
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        ride = Ride.objects.get(id=ride_id, usn=request.user)
    except Ride.DoesNotExist:
        messages.error(request, "Ride not found or you are not authorized to cancel it.")
        return redirect('ridemate_profile')
    
    # Check if it's a GET request (confirmation page) or POST (actual cancellation)
    if request.method == 'POST':
        # Get all ride requests
        ride_requests = RideRequest.objects.filter(ride=ride, status="Accepted")
        
        # Notify all accepted passengers about cancellation
        for req in ride_requests:
            req.status = "Cancelled"
            req.save()
        
        # Delete the ride
        ride.delete()
        
        messages.success(request, "Your ride has been cancelled successfully.")
        return redirect('ridemate_profile')
    
    # Show confirmation page
    return render(request, 'cancel_ride.html', {'ride': ride})

def cancel_booking(request, request_id):
    """View for cancelling a ride booking."""
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        ride_request = RideRequest.objects.get(id=request_id, requestor=request.user)
    except RideRequest.DoesNotExist:
        messages.error(request, "Booking not found or you are not authorized to cancel it.")
        return redirect('ridemate_profile')
    
    # Check if it's a GET request (confirmation page) or POST (actual cancellation)
    if request.method == 'POST':
        # Update the ride request
        ride_request.status = "Cancelled"
        ride_request.save()
        
        # Update available seats on the ride
        ride = ride_request.ride
        ride.available_seats += 1
        ride.save()
        
        messages.success(request, "Your booking has been cancelled successfully.")
        return redirect('ridemate_profile')
    
    # Show confirmation page
    return render(request, 'cancel_booking.html', {'request': ride_request})

def ride_requests(request, ride_id):
    """View for managing ride requests for a specific ride."""
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        ride = Ride.objects.get(id=ride_id, usn=request.user)
    except Ride.DoesNotExist:
        messages.error(request, "Ride not found or you are not authorized to view requests.")
        return redirect('ridemate_profile')
    
    # Get all requests for this ride
    pending_requests = RideRequest.objects.filter(ride=ride, status="Pending").select_related('requestor')
    accepted_requests = RideRequest.objects.filter(ride=ride, status="Accepted").select_related('requestor')
    
    context = {
        'ride': ride,
        'pending_requests': pending_requests,
        'accepted_requests': accepted_requests
    }
    
    return render(request, 'ride_requests.html', context)

def handle_request(request, request_id, action):
    """View for accepting or rejecting a ride request."""
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        ride_request = RideRequest.objects.get(id=request_id, ride__usn=request.user)
    except RideRequest.DoesNotExist:
        messages.error(request, "Request not found or you are not authorized to handle it.")
        return redirect('ridemate_profile')
    
    ride = ride_request.ride
    
    if action == 'accept':
        # Check if there are enough seats
        if ride.available_seats <= 0:
            messages.error(request, "No seats available on this ride.")
            return redirect('ride_requests', ride_id=ride.id)
        
        # Accept the request
        ride_request.status = "Accepted"
        ride_request.save()
        
        # Update available seats
        ride.available_seats -= 1
        ride.save()
        
        messages.success(request, "Request accepted successfully.")
    
    elif action == 'reject':
        # Reject the request
        ride_request.status = "Rejected"
        ride_request.save()
        
        messages.success(request, "Request rejected successfully.")
    
    return redirect('ride_requests', ride_id=ride.id)