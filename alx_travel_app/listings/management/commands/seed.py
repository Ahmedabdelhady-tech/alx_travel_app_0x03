from django.core.management.base import BaseCommand
from listings.models import Listing, Booking, Review
import random
from datetime import timedelta, date
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = "Seed the database with sample listings, bookings, and reviews"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")

        # Clear existing data
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Listing.objects.all().delete()

        for _ in range(10):
            listing = Listing.objects.create(
                title=fake.sentence(nb_words=4),
                description=fake.text(),
                price_per_night=random.randint(100, 1000),
                location=fake.city(),
            )

            booking = Booking.objects.create(
                listing=listing,
                guest_name=fake.name(),
                check_in=date.today(),
                check_out=date.today() + timedelta(days=3),
            )

            Review.objects.create(
                listing=listing, rating=random.randint(1, 5), comment=fake.text()
            )

        self.stdout.write(self.style.SUCCESS("✅ Database seeded successfully!"))
