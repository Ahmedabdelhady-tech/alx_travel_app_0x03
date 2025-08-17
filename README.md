# 🧳 ALX Travel App 0x01

This project is part of the ALX backend specialization. It is a Django-based travel app that manages listings, bookings, and reviews with database seeding capabilities.

## 🚀 Features

- List travel destinations
- Book listings with date ranges
- Add reviews with ratings
- Seed the database with random data using `Faker`

## 🛠️ Tech Stack

- Python 3
- Django
- Django REST Framework
- MySQL

## 📁 Project Structure

alx_travel_app/
├── listings/
│ ├── models.py
│ ├── serializers.py
│ ├── management/
│ │ └── commands/
│ │ └── seed.py
├── alx_travel_app/
│ └── settings.py
├── manage.py

## 🧬 Models

### Listing

- `title`: CharField
- `description`: TextField
- `price`: IntegerField
- `location`: CharField

### Booking

- `listing`: ForeignKey → Listing
- `guest_name`: CharField
- `check_in`: DateField
- `check_out`: DateField

### Review

- `listing`: ForeignKey → Listing
- `rating`: IntegerField (1–5)
- `comment`: TextField

## 🧪 Seed Command-

To populate the database with sample data:

```bash
python manage.py seed

