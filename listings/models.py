from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# -------------------------
# Custom User
# -------------------------
class CustomUser(AbstractUser):
    """Custom user model that uses email as the login field."""
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_image = models.URLField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


# -------------------------
# Listing (like an Airbnb property)
# -------------------------
class Listing(models.Model):
    host = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="listings")
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.location}"


# -------------------------
# Booking (when a user books a property)
# -------------------------
class Booking(models.Model):
    property = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[('PENDING', 'Pending'), ('CONFIRMED', 'Confirmed'), ('CANCELLED', 'Cancelled')],
        default='PENDING'
    )

    def __str__(self):
        return f"Booking {self.id} - {self.property.name}"

    def clean(self):
        """Basic validation: end date after start date and not in the past."""
        if self.start_date and self.end_date:
            if self.start_date >= self.end_date:
                raise ValueError("End date must be after start date")
            if self.start_date < timezone.now().date():
                raise ValueError("Start date cannot be in the past")


# -------------------------
# Review (user feedback on a listing)
# -------------------------
class Review(models.Model):
    property = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField()  # keep simple, no validators for now
    comment = models.TextField()

    def __str__(self):
        return f"Review by {self.user.username} - {self.rating}/5"


# -------------------------
# Payment Model for Chapa Integration
# -------------------------
class Payment(models.Model):
    # Status choices help us maintain data integrity by limiting what values are valid
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    # The booking this payment is associated with
    # We use ForeignKey because one booking has one payment, but we might query payments by booking
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE, related_name='payments')
    
    # Financial information
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='ETB')  # Ethiopian Birr is Chapa's primary currency
    
    # Transaction tracking
    # This is the unique identifier Chapa gives us to track this specific payment
    transaction_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    
    # Chapa's reference for this transaction
    chapa_reference = models.CharField(max_length=255, unique=True, null=True, blank=True)
    
    # Current status of the payment
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Timestamps help us track when things happened and debug issues
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Store the full response from Chapa for debugging and record-keeping
    chapa_response = models.JSONField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Payment {self.transaction_id} - {self.status}"
