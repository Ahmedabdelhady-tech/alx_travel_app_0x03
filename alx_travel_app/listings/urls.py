from django.urls import path, include
from .views import ListingViewSet, BookingViewSet
from rest_framework.routers import DefaultRouter
from .views import InitiatePaymentView, VerifyPaymentView

router = DefaultRouter()
router.register(r"listings", ListingViewSet, basename="listing")
router.register(r"booking", BookingViewSet, basename="booking")

urlpatterns = [
    path("", include(router.urls)),
    path("payments/initiate/", InitiatePaymentView.as_view(), name="initiate-payment"),
    path("payments/verify/", VerifyPaymentView.as_view(), name="verify-payment"),
]
