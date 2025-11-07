from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from listings.models import Listing, Booking, Review
from listings.enums import Status
import random
from datetime import timedelta

User = get_user_model()

class Command(BaseCommand):
    help = "Seed the database with sample listings, bookings, and reviews"

    def handle(self, *args, **kwargs):
        # --- USERS ---
        host, _ = User.objects.get_or_create(
            email="host@example.com",
            defaults={
                "username": "hostuser",
                "password": "password123",  # not hashed (demo only)
            },
        )

        user, _ = User.objects.get_or_create(
            email="guest@example.com",
            defaults={
                "username": "guestuser",
                "password": "password123",
            },
        )

        self.stdout.write(self.style.SUCCESS("Demo users created."))

        # --- LISTINGS ---
        sample_listings = [
            {
                "name": "Cozy Apartment in City Center",
                "description": "A lovely apartment near restaurants and shops.",
                "location": "Downtown",
                "price_per_night": 75.00,
            },
            {
                "name": "Luxury Villa with Pool",
                "description": "Spacious villa with private swimming pool and garden.",
                "location": "Beverly Hills",
                "price_per_night": 350.00,
            },
            {
                "name": "Mountain Cabin Retreat",
                "description": "Peaceful cabin with stunning mountain views.",
                "location": "Rocky Mountains",
                "price_per_night": 120.00,
            },
        ]

        listings = []
        for data in sample_listings:
            listing, _ = Listing.objects.get_or_create(
                host=host,
                name=data["name"],
                defaults={
                    "description": data["description"],
                    "location": data["location"],
                    "price_per_night": data["price_per_night"],
                    "is_available": True,
                },
            )
            listings.append(listing)

        self.stdout.write(self.style.SUCCESS("Sample listings created."))

        # --- BOOKINGS ---
        for listing in listings:
            start_date = timezone.now().date() + timedelta(days=random.randint(1, 10))
            end_date = start_date + timedelta(days=random.randint(2, 5))
            total_price = (end_date - start_date).days * listing.price_per_night

            Booking.objects.get_or_create(
                property=listing,
                user=user,
                start_date=start_date,
                end_date=end_date,
                defaults={
                    "total_price": total_price,
                    "status": random.choice([Status.CONFIRMED, Status.PENDING]),
                },
            )

        self.stdout.write(self.style.SUCCESS("Sample bookings created."))

        # --- REVIEWS ---
        for listing in listings:
            Review.objects.get_or_create(
                property=listing,
                user=user,
                defaults={
                    "rating": random.randint(3, 5),
                    "comment": f"Great place! Loved staying at {listing.name}.",
                },
            )

        self.stdout.write(self.style.SUCCESS("Sample reviews created."))
        self.stdout.write(self.style.SUCCESS("Database seeding complete! 🚀"))
