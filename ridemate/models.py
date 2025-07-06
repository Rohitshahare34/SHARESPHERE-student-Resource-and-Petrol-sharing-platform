from django.db import models
from login.models import Users  # Import Users model for foreign key
from django.utils import timezone
import datetime
from django.contrib.auth.models import User

# Create your models here.
class Ride(models.Model):
    GENDER_CHOICES = [
        ('any', 'Any'),
        ('male', 'Male Only'),
        ('female', 'Female Only'),
    ]
    
    usn = models.ForeignKey(Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    destination = models.CharField(max_length=200)
    seats_available = models.PositiveIntegerField()
    contact_number = models.CharField(max_length=15)
    
    # New fields
    ride_datetime = models.DateTimeField(default=timezone.now)
    pickup_location = models.CharField(max_length=200, default='Campus')
    dropoff_points = models.TextField(blank=True, null=True)
    price_per_seat = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    gender_preference = models.CharField(max_length=10, choices=GENDER_CHOICES, default='any')
    vehicle_number = models.CharField(max_length=20, blank=True, null=True)
    additional_notes = models.TextField(blank=True, null=True)
    
    # Auto-cancel feature fields
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_time = models.DateTimeField(default=timezone.now() + datetime.timedelta(hours=2))
    is_booked = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.destination}"
    
    def save(self, *args, **kwargs):
        # Set expiry time to 2 hours after creation if not provided
        if not self.expiry_time:
            self.expiry_time = timezone.now() + datetime.timedelta(hours=2)
        
        # Check if ride is expired
        current_time = timezone.now()
        if current_time >= self.expiry_time:
            self.is_expired = True
        
        super().save(*args, **kwargs)
    
    def is_active(self):
        """Check if the ride is still active (not expired and not fully booked)"""
        current_time = timezone.now()
        if current_time >= self.expiry_time:
            self.is_expired = True
            self.save()
        return not self.is_expired and not self.is_booked and current_time < self.expiry_time

    class Meta:
        ordering = ['-created_at']


    
  

class RidePreferences(models.Model):
    """Model to store user ride preferences."""
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='ride_preferences')
    common_destinations = models.TextField(blank=True, null=True, help_text="Comma-separated list of common destinations")
    preferred_morning = models.TimeField(blank=True, null=True, help_text="Preferred morning departure time")
    preferred_evening = models.TimeField(blank=True, null=True, help_text="Preferred evening departure time")
    vehicle_model = models.CharField(max_length=100, blank=True, null=True, help_text="Vehicle model information")
    vehicle_number = models.CharField(max_length=20, blank=True, null=True, help_text="Vehicle registration number")
    music_allowed = models.BooleanField(default=True, help_text="Whether music is allowed during rides")
    smoking_allowed = models.BooleanField(default=False, help_text="Whether smoking is allowed during rides")
    pets_allowed = models.BooleanField(default=False, help_text="Whether pets are allowed during rides")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Preferences for {self.user.name}"

class RideRequest(models.Model):
    """Model to handle ride booking requests."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='requests')
    requester = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='ride_requests')
    seats_requested = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.requester.name}'s request for {self.ride}"

class RideFeedback(models.Model):
    """Model to store feedback for completed rides."""
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # 1-5 star rating
    
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_driver_feedback = models.BooleanField(default=False)  # True if feedback is for driver, False if for rider
    
    def __str__(self):
        return f"{'Driver' if self.is_driver_feedback else 'Rider'} feedback for {self.ride}"

    class Meta:
        unique_together = ['ride', 'user', 'is_driver_feedback']  # One feedback per user per ride per type

class RideMateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ridemate_profile')
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='ridemate_profile_pics/', blank=True, null=True)
    preferred_pickup_locations = models.CharField(max_length=255, blank=True)
    preferred_destinations = models.CharField(max_length=255, blank=True)
    vehicle_number = models.CharField(max_length=50, blank=True)
    vehicle_type = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    ride_count = models.PositiveIntegerField(default=0)
    avg_rating = models.FloatField(default=0.0)
    is_driver = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}'s RideMate Profile"

class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    year = models.CharField(max_length=10)
    feedback_text = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
