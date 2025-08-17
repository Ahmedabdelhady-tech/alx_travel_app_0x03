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
