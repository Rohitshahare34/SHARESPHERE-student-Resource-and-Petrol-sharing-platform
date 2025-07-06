from django.db import models
from login.models import Users
from datetime import date

class Items(models.Model):
    item_id = models.CharField(max_length=20, unique=True, primary_key=True)  # Primary Key
    usn = models.ForeignKey(Users, on_delete=models.CASCADE)  # User reference
    product_name = models.CharField(max_length=100)
    
    CATEGORY_CHOICES = [
        ('Tools', 'Tools'),
        ('Study', 'Study'),
        ('Clothing', 'Clothing'),
        ('Electronics', 'Electronics'),
        ('Others', 'Others'),
    ]
    product_category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    product_description = models.TextField()
    price = models.PositiveIntegerField()
    photo = models.ImageField(upload_to='product_images/')
    
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Sold', 'Sold'),
    ]
    availability_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Available')

    class Meta:
        db_table = 'buysell_items'

    def save(self, *args, **kwargs):
        if not self.item_id:
            count = Items.objects.filter(usn=self.usn).count() + 1  # Fix auto-increment
            self.item_id = f"{self.usn.usn}-{count}"  # Ensure usn is a string
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_name} ({self.availability_status})"

    
class Cart(models.Model):
    cart_id = models.CharField(max_length=50, unique=True, primary_key=True)  # Primary Key
    item = models.ForeignKey(Items, on_delete=models.CASCADE)  # Reference to Items table
    usn = models.ForeignKey(Users, on_delete=models.CASCADE)  # Reference to Users table
    date_added = models.DateField(default=date.today)

    class Meta:
        db_table = 'buysell_cart'

    def save(self, *args, **kwargs):
        if not self.cart_id:
            count = Cart.objects.filter(usn=self.usn).count() + 1  # Fix auto-increment
            self.cart_id = f"CI_{self.usn.usn}_{count}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"CartItem: {self.cart_id} - {self.item.product_name}"

class Wishlist(models.Model):
    wishlist_id = models.CharField(max_length=50, unique=True, primary_key=True)  # Primary Key
    item = models.ForeignKey(Items, on_delete=models.CASCADE)  # Reference to Items table
    usn = models.ForeignKey(Users, on_delete=models.CASCADE)  # Reference to Users table
    date_added = models.DateField(default=date.today)

    class Meta:
        db_table = 'buysell_wishlist'
        unique_together = ('item', 'usn')  # Prevent duplicate wishlist entries

    def save(self, *args, **kwargs):
        if not self.wishlist_id:
            count = Wishlist.objects.filter(usn=self.usn).count() + 1
            self.wishlist_id = f"WL_{self.usn.usn}_{count}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"WishlistItem: {self.wishlist_id} - {self.item.product_name}"
