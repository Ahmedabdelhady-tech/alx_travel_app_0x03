from django.shortcuts import render
from .models import Listing, Booking, Payment
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from .serializers import ListingSerializer, BookingSerializer
import uuid
import requests
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings


class ListingListCreateAPIView(ListCreateAPIView):
    def list(self, request, *args, **kwargs):
        return Response({"detail": "This is your listings endpoint"})

    def create(self, request, *args, **kwargs):
        return Response({"detail": "Create a listing"})


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class InitiatePaymentView(APIView):
    def post(self, request):
        booking_id = request.data.get("booking_id")
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
        except Booking.DoesNotExist:
            return Response(
                {"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND
            )

        tx_ref = str(uuid.uuid4())
        payment = Payment.objects.create(
            booking=booking,
            user=request.user,
            amount=booking.total_amount,
            chapa_tx_ref=tx_ref,
        )

        payload = {
            "amount": booking.total_amount,
            "currency": "ETB",
            "tx_ref": tx_ref,
            "callback_url": "https://yourdomain.com/api/payments/verify/",
            "customer_email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
        }
        headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}
        response = requests.post(
            "https://api.chapa.co/v1/transaction/initialize",
            json=payload,
            headers=headers,
        )

        if response.status_code == 200:
            data = response.json()["data"]
            return Response({"checkout_url": data["checkout_url"]})
        else:
            payment.status = "failed"
            payment.save()
            return Response(
                {"error": "Payment initiation failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class VerifyPaymentView(APIView):
    def get(self, request):
        tx_ref = request.GET.get("tx_ref")
        try:
            payment = Payment.objects.get(chapa_tx_ref=tx_ref)
        except Payment.DoesNotExist:
            return Response(
                {"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND
            )

        headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}
        response = requests.get(
            f"https://api.chapa.co/v1/transaction/verify/{tx_ref}", headers=headers
        )

        if response.status_code == 200:
            data = response.json()["data"]
            if data["status"] == "success":
                payment.status = "successful"
                payment.save()

                from .tasks import send_payment_confirmation_email

                send_payment_confirmation_email.delay(payment.id)
                return Response({"status": "Payment successful"})
            else:
                payment.status = "failed"
                payment.save()
                return Response(
                    {"status": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"error": "Verification failed"}, status=status.HTTP_400_BAD_REQUEST
            )
