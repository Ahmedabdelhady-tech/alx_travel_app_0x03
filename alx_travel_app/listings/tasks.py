from celery import shared_task
from django.core.mail import send_mail
from .models import Payment


@shared_task
def send_payment_confirmation_email(payment_id):
    payment = Payment.objects.get(id=payment_id)
    send_mail(
        "Payment Confirmation",
        f"Your payment of {payment.amount} for booking #{payment.booking.id} was successful.",
        "no-reply@travelapp.com",
        [payment.user.email],
    )

from django.conf import settings


@shared_task
def send_booking_confirmation_email(user_email, booking_id):
    subject = "Booking Confirmation"
    message = f"Your booking with ID {booking_id} has been confirmed!"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
    return f"Email sent to {user_email} for booking {booking_id}"
