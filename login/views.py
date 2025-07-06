from django.shortcuts import render, redirect
from django.http import HttpResponse
from login.models import Users  # Ensure correct import
from ridemate.models import Testimonial  # Import Testimonial model
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.conf import settings
import random
import string
import logging

def user_login(request):
    if request.method == "POST":
        usn = request.POST.get("usn").strip()
        password = request.POST.get("password").strip()

        try:
            user = Users.objects.get(usn=usn)
            if user.password.strip() == password:
                # Store user's ID in session
                request.session['user_usn'] = user.usn
                return redirect("home")  # Redirect to home page
            else:
                return render(request, "login.html", {"error": "Invalid USN or password"})
        except Users.DoesNotExist:
            return render(request, "login.html", {"error": "Invalid USN or password"})

    return render(request, "login.html")

def home_view(request):
    if 'user_usn' not in request.session:
        return redirect('login') 
    
    # Get all approved testimonials to display on the homepage
    testimonials = Testimonial.objects.filter(is_approved=True).order_by('-created_at')
    
    context = {
        'testimonials': testimonials,
        'user_usn': request.session.get('user_usn')
    }
    
    return render(request, "home.html", context)


def user_logout(request):
    request.session.flush()  # Clear all session data
    return redirect('login')

def logout_user(request):
    logout(request)
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        usn = request.POST.get('usn')
        name = request.POST.get('name')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        contact_number = request.POST.get('contact_number')
        department_name = request.POST.get('department_name')
        year = request.POST.get('year')
        semester = request.POST.get('semester')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validate password match
        if password != confirm_password:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})

        # Check if USN already exists
        if Users.objects.filter(usn=usn).exists():
            return render(request, 'signup.html', {'error': 'USN already exists'})

        # Check if email already exists
        if Users.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already exists'})

        try:
            # Create new user
            user = Users.objects.create(
                usn=usn,
                name=name,
                email=email,
                dob=dob,
                contact_number=contact_number,
                department_name=department_name,
                year=year,
                semester=semester,
                password=password  # Note: In production, you should hash the password
            )
            
            # Redirect to login page with success message
            return redirect('login')
        except Exception as e:
            return render(request, 'signup.html', {'error': str(e)})

    return render(request, 'signup.html')

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def forgot_password(request):
    return render(request, 'forgot_password.html', {'step': 1})

def send_otp(request):
    if request.method == 'POST':
        identifier = request.POST.get('usn').strip()
        try:
            # Try to find user by USN first
            try:
                user = Users.objects.get(usn=identifier)
            except Users.DoesNotExist:
                # If not found by USN, try email
                user = Users.objects.get(email=identifier)
            
            # Generate OTP
            otp = generate_otp()
            # Store OTP in session
            request.session['reset_otp'] = otp
            request.session['reset_usn'] = user.usn  # Store USN for later use
            
            # Send OTP via email
            subject = 'ShareSphere Password Reset OTP'
            message = f'''Your OTP for password reset is: {otp}
            
This OTP will expire in 10 minutes.
            
Best regards,
ShareSphere Team'''
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                return render(request, 'forgot_password.html', {
                    'step': 2,
                    'success': 'OTP has been sent to your email'
                })
            except Exception as e:
                logger = logging.getLogger('login')
                logger.error(f'Failed to send email: {str(e)}')
                return render(request, 'forgot_password.html', {
                    'step': 1,
                    'error': 'Failed to send OTP. Please try again.'
                })
                
        except Users.DoesNotExist:
            return render(request, 'forgot_password.html', {
                'step': 1,
                'error': 'No account found with this USN/Email'
            })
    
    return redirect('forgot_password')

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('reset_otp')
        
        if not stored_otp:
            return render(request, 'forgot_password.html', {
                'step': 1,
                'error': 'OTP has expired. Please request a new one.'
            })
        
        if entered_otp == stored_otp:
            # OTP is valid, move to reset password step
            return render(request, 'forgot_password.html', {'step': 3})
        else:
            return render(request, 'forgot_password.html', {
                'step': 2,
                'error': 'Invalid OTP. Please try again.'
            })
    
    return redirect('forgot_password')

def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        usn = request.session.get('reset_usn')
        
        if not usn:
            return redirect('forgot_password')
        
        if new_password != confirm_password:
            return render(request, 'forgot_password.html', {
                'step': 3,
                'error': 'Passwords do not match'
            })
        
        try:
            user = Users.objects.get(usn=usn)
            user.password = new_password  # In production, hash the password
            user.save()
            
            # Clear session data
            del request.session['reset_otp']
            del request.session['reset_usn']
            
            return render(request, 'login.html', {
                'success': 'Password has been reset successfully'
            })
            
        except Users.DoesNotExist:
            return render(request, 'forgot_password.html', {
                'step': 1,
                'error': 'Something went wrong. Please try again.'
            })
    
    return redirect('forgot_password')
