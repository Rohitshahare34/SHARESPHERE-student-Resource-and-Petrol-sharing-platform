from django.shortcuts import render, redirect
from .models import Items
from django.contrib import messages  # For error messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from login.models import Users  # Ensure correct import of Users model
from BuySell.models import Items, Cart, Wishlist
from time import time
from django.utils.timezone import now
from django.shortcuts import render, redirect
from django.db.models import Q
import json
from django.utils import timezone
from django.db.models import Count, Avg
from ridemate.models import Ride, RideRequest, RideFeedback
from datetime import datetime


# Create your views here.
# def home(request):
#     items = Items.objects.filter(availability_status="Available")  # Fetch only available items
#     return render(request, "BuySell_home.html", {"items": items})

# my code
def home(request):
    # Get search parameters from request
    search_query = request.GET.get('search_query', '')
    category = request.GET.get('category', 'All')
    
    # Get all available items and order by item_id (which contains sequential numbers)
    items = Items.objects.filter(availability_status="Available").order_by('-item_id')[:10]  # Show only 10 most recent items
    
    # List of categories for filter options
    categories = ["All", "Electronics", "Study", "Vehicles", "Clothing", "Tools"]
    
    # Get user's cart items if logged in
    cart_items = []
    cart_total = 0
    cart_item_ids = []
    
    # Get user's wishlist items if logged in
    wishlist_items = []
    wishlist_item_ids = []
    
    if 'user_usn' in request.session:
        user_usn = request.session.get('user_usn')
        try:
            user = Users.objects.get(usn=user_usn)
            
            # Fetch cart items
            cart_entries = Cart.objects.filter(usn=user).select_related('item')
            for entry in cart_entries:
                cart_items.append({
                    'cart_id': entry.cart_id,
                    'item_id': entry.item.item_id,
                    'name': entry.item.product_name,
                    'price': entry.item.price,
                    'photo_url': entry.item.photo.url if entry.item.photo else '',
                    'category': entry.item.product_category
                })
                cart_item_ids.append(entry.item.item_id)
                cart_total += entry.item.price
                
            # Fetch wishlist items
            wishlist_entries = Wishlist.objects.filter(usn=user).select_related('item')
            for entry in wishlist_entries:
                wishlist_items.append({
                    'wishlist_id': entry.wishlist_id,
                    'item_id': entry.item.item_id,
                    'name': entry.item.product_name,
                    'price': entry.item.price,
                    'photo_url': entry.item.photo.url if entry.item.photo else '',
                    'category': entry.item.product_category
                })
                wishlist_item_ids.append(entry.item.item_id)
                
        except Users.DoesNotExist:
            pass
    
    context = {
        'items': items,
        'categories': categories,
        'selected_category': category,
        'search_query': search_query,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_count': len(cart_items),
        'cart_item_ids': json.dumps(cart_item_ids),
        'wishlist_items': wishlist_items,
        'wishlist_count': len(wishlist_items),
        'wishlist_item_ids': json.dumps(wishlist_item_ids)
    }
    
    return render(request, 'BuySell_home.html', context)


def sell_product(request):
    return render(request,'BuySell_sell_product.html')


def upload_item(request):
    if request.method == "POST":
        product_name = request.POST.get("product_name")
        product_category = request.POST.get("product_category")
        product_description = request.POST.get("product_description")
        price = request.POST.get("price")
        photo = request.FILES.get("photo")

        if not all([product_name, product_category, product_description, price, photo]):
            messages.error(request, "All fields are required.")
            return redirect("sell_product")

        try:
            price = int(price)  # Ensure price is an integer
        except ValueError:
            messages.error(request, "Invalid price format.")
            return redirect("sell_product")

        # Fetch the logged-in user using session data
        user_usn = request.session.get("user_usn")  # Get USN from session
        if not user_usn:
            messages.error(request, "User not authenticated.")
            return redirect("login")

        try:
            user = Users.objects.get(usn=user_usn)  # Get Users instance
        except Users.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect("login")

        try:
            # Generate a unique item_id
            user_items_count = Items.objects.filter(usn=user).count() + 1
            item_id = f"{user.usn}-{user_items_count}"

            # Create and save the item
            new_item = Items.objects.create(
                item_id=item_id,
                usn=user,  # Pass the actual Users instance
                product_name=product_name,
                product_category=product_category,
                product_description=product_description,
                price=price,
                photo=photo,
                availability_status="Available"
            )
            
            messages.success(request, "Item uploaded successfully!")
            return redirect('buysell_home')

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect("sell_product")

    return redirect("sell_product")

def add_to_cart(request):
    if "user_usn" not in request.session:
        return JsonResponse({"success": False, "message": "User not authenticated."})

    if request.method == "POST":
        item_id = request.POST.get("item_id")
        if not item_id:
            return JsonResponse({"success": False, "message": "Item ID missing!"})

        try:
            item = Items.objects.get(item_id=item_id)
            user_usn = request.session["user_usn"]  
            user = Users.objects.get(usn=user_usn)
            
            # Check if item is already in cart
            if Cart.objects.filter(item=item, usn=user).exists():
                return JsonResponse({"success": False, "message": "Item already in cart"})
            
            # Add to cart
            cart_item = Cart.objects.create(item=item, usn=user)

            # Return item details for updating UI
            return JsonResponse({
                "success": True, 
                "message": "Item added to cart",
                "item": {
                    "cart_id": cart_item.cart_id,
                    "item_id": item.item_id,
                    "name": item.product_name,
                    "price": item.price,
                    "photo_url": item.photo.url if item.photo else '',
                    "category": item.product_category
                }
            })
        except Items.DoesNotExist:
            return JsonResponse({"success": False, "message": "Item not found!"})
        except Users.DoesNotExist:
            return JsonResponse({"success": False, "message": "User not found!"})
    
    return JsonResponse({"success": False, "message": "Invalid request!"})

def remove_from_cart(request):
    if "user_usn" not in request.session:
        return JsonResponse({"success": False, "message": "User not authenticated."})
        
    if request.method == "POST":
        cart_id = request.POST.get("cart_id")
        if not cart_id:
            return JsonResponse({"success": False, "message": "Cart ID missing!"})
            
        try:
            cart_item = Cart.objects.get(cart_id=cart_id)
            
            # Verify that the cart item belongs to the logged-in user
            user_usn = request.session["user_usn"]
            user = Users.objects.get(usn=user_usn)
            
            if cart_item.usn != user:
                return JsonResponse({"success": False, "message": "Unauthorized access!"})
                
            # Delete the cart item
            cart_item.delete()
            return JsonResponse({"success": True, "message": "Item removed from cart"})
            
        except Cart.DoesNotExist:
            return JsonResponse({"success": False, "message": "Cart item not found!"})
        except Users.DoesNotExist:
            return JsonResponse({"success": False, "message": "User not found!"})
            
    return JsonResponse({"success": False, "message": "Invalid request!"})

def profile(request):
    if "user_usn" not in request.session:
        return redirect('login')
    
    user_usn = request.session.get("user_usn")
    try:
        user = Users.objects.get(usn=user_usn)
        
        # BuySell Statistics
        items_listed = Items.objects.filter(usn=user).count()
        items_sold = Items.objects.filter(usn=user, availability_status='Sold').count()
        items_bought = Cart.objects.filter(usn=user).count()
        
        # Recent BuySell Activity
        recent_purchases = Cart.objects.filter(usn=user).order_by('-cart_id')[:5]  # Using cart_id for ordering
        recent_sales = Items.objects.filter(usn=user, availability_status='Sold').order_by('-item_id')[:5]  # Using item_id for ordering
        listed_items = Items.objects.filter(usn=user).order_by('-item_id')[:6]  # Using item_id for ordering
        
        # RideMate Statistics
        rides_offered = Ride.objects.filter(usn=user).count()
        rides_taken = RideRequest.objects.filter(
            requester=user, 
            status='accepted'
        ).count()
        
        # Initialize ratings with default values
        driver_rating = 0
        rider_rating = 0
        
        try:
            # Try to calculate ratings if the table exists
            driver_rating = RideFeedback.objects.filter(
                ride__usn=user,
                is_driver_feedback=True
            ).aggregate(Avg('rating'))['rating__avg'] or 0
            
            rider_rating = RideFeedback.objects.filter(
                user=user,
                is_driver_feedback=False
            ).aggregate(Avg('rating'))['rating__avg'] or 0
        except Exception:
            # If the table doesn't exist or there's any other error, use default values
            pass
        
        # Recent RideMate Activity
        recent_rides_offered = Ride.objects.filter(
            usn=user
        ).order_by('-created_at')[:5]
        
        recent_rides_taken = RideRequest.objects.filter(
            requester=user,
            status='accepted'
        ).order_by('-created_at')[:5]
        
        # Active Rides
        active_rides_offered = Ride.objects.filter(
            usn=user,
            is_expired=False,
            is_booked=False,
            expiry_time__gt=timezone.now()
        )
        
        active_ride_requests = RideRequest.objects.filter(
            requester=user,
            status='pending'
        )
        
        context = {
            'user': user,
            # BuySell Stats
            'items_listed': items_listed,
            'items_sold': items_sold,
            'items_bought': items_bought,
            'recent_purchases': recent_purchases,
            'recent_sales': recent_sales,
            'listed_items': listed_items,
            # RideMate Stats
            'rides_offered': rides_offered,
            'rides_taken': rides_taken,
            'driver_rating': round(driver_rating, 1),
            'rider_rating': round(rider_rating, 1),
            'recent_rides_offered': recent_rides_offered,
            'recent_rides_taken': recent_rides_taken,
            'active_rides_offered': active_rides_offered,
            'active_ride_requests': active_ride_requests,
        }
        return render(request, 'profile.html', context)
        
    except Users.DoesNotExist:
        messages.error(request, "User not found")
        return redirect('login')

def edit_profile(request):
    if "user_usn" not in request.session:
        return redirect("login")
    
    user_usn = request.session.get("user_usn")
    try:
        user = Users.objects.get(usn=user_usn)
        
        if request.method == "POST":
            # Get form data
            name = request.POST.get("name")
            email = request.POST.get("email")
            contact_number = request.POST.get("contact_number")
            year = request.POST.get("year")
            semester = request.POST.get("semester")
            department_name = request.POST.get("department_name")
            profile_picture = request.FILES.get("profile_picture")
            
            # Validate required fields
            if not all([name, email, contact_number, year, semester, department_name]):
                messages.error(request, "All fields are required.")
                return redirect("edit_profile")
            
            try:
                # Update user fields
                user.name = name
                user.email = email
                user.contact_number = contact_number
                user.year = int(year)
                user.semester = int(semester)
                user.department_name = department_name
                
                # Handle password change if provided
                current_password = request.POST.get("current_password")
                new_password = request.POST.get("new_password")
                confirm_password = request.POST.get("confirm_password")
                
                if current_password and new_password and confirm_password:
                    # Verify current password
                    if not user.check_password(current_password):
                        messages.error(request, "Current password is incorrect.")
                        return redirect("edit_profile")
                    
                    # Validate new password
                    if new_password != confirm_password:
                        messages.error(request, "New passwords do not match.")
                        return redirect("edit_profile")
                    
                    # Set new password
                    user.set_password(new_password)
                    messages.success(request, "Password updated successfully.")
                
                # Handle profile picture upload
                if profile_picture:
                    user.profile_picture = profile_picture
                
                user.save()
                messages.success(request, "Profile updated successfully!")
                return redirect("profile")
                
            except ValueError as e:
                messages.error(request, f"Invalid input: {str(e)}")
                return redirect("edit_profile")
            except Exception as e:
                messages.error(request, f"Error updating profile: {str(e)}")
                return redirect("edit_profile")
        
        context = {
            'user': user
        }
        return render(request, "edit_profile.html", context)
        
    except Users.DoesNotExist:
        return redirect("login")

def add_to_wishlist(request):
    if "user_usn" not in request.session:
        return JsonResponse({"success": False, "message": "User not authenticated."})

    if request.method == "POST":
        item_id = request.POST.get("item_id")
        if not item_id:
            return JsonResponse({"success": False, "message": "Item ID missing!"})

        try:
            item = Items.objects.get(item_id=item_id)
            user_usn = request.session["user_usn"]  
            user = Users.objects.get(usn=user_usn)
            
            # Check if item is already in wishlist
            if Wishlist.objects.filter(item=item, usn=user).exists():
                return JsonResponse({"success": False, "message": "Item already in wishlist"})
            
            # Add to wishlist
            wishlist_item = Wishlist.objects.create(item=item, usn=user)

            # Return item details for updating UI
            return JsonResponse({
                "success": True, 
                "message": "Item added to wishlist",
                "item": {
                    "wishlist_id": wishlist_item.wishlist_id,
                    "item_id": item.item_id,
                    "name": item.product_name,
                    "price": item.price,
                    "photo_url": item.photo.url if item.photo else '',
                    "category": item.product_category
                }
            })
        except Items.DoesNotExist:
            return JsonResponse({"success": False, "message": "Item not found!"})
        except Users.DoesNotExist:
            return JsonResponse({"success": False, "message": "User not found!"})
    
    return JsonResponse({"success": False, "message": "Invalid request!"})

def remove_from_wishlist(request):
    if "user_usn" not in request.session:
        return JsonResponse({"success": False, "message": "User not authenticated."})
        
    if request.method == "POST":
        wishlist_id = request.POST.get("wishlist_id")
        if not wishlist_id:
            return JsonResponse({"success": False, "message": "Wishlist ID missing!"})
            
        try:
            wishlist_item = Wishlist.objects.get(wishlist_id=wishlist_id)
            
            # Verify that the wishlist item belongs to the logged-in user
            user_usn = request.session["user_usn"]
            user = Users.objects.get(usn=user_usn)
            
            if wishlist_item.usn != user:
                return JsonResponse({"success": False, "message": "Unauthorized access!"})
                
            # Delete the wishlist item
            wishlist_item.delete()
            return JsonResponse({"success": True, "message": "Item removed from wishlist"})
            
        except Wishlist.DoesNotExist:
            return JsonResponse({"success": False, "message": "Wishlist item not found!"})
        except Users.DoesNotExist:
            return JsonResponse({"success": False, "message": "User not found!"})
            
    return JsonResponse({"success": False, "message": "Invalid request!"})
        