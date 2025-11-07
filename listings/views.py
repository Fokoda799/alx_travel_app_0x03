from rest_framework import viewsets
from .models import Listing, Booking, Review
from .serializers import ListingSerializer, BookingSerializer, ReviewSerializer
from .tasks import send_booking_confirmation_email


class ListingsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Listing model.
    Provides: list, create, retrieve, update, destroy actions automatically.
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class BookingsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Booking model.
    Provides: list, create, retrieve, update, destroy actions automatically.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        """
        Override the create method to trigger the email task after
        a booking is successfully created.
        """
        # First, create the booking using the standard process
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Get the created booking instance
        booking = serializer.instance
        
        # Trigger the email task asynchronously
        # The .delay() method sends the task to Celery without waiting for it to complete
        # This means your API responds immediately while the email is sent in the background
        send_booking_confirmation_email.delay(
            booking_id=booking.id,
            user_email=booking.user.email,
            listing_title=booking.property.name,
            check_in=str(booking.start_date),
            check_out=str(booking.end_date)
        )
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class ReviewViewSet(viewsets.ModelViewSet):
  queryset = Review.objects.all()
  serializer_class = ReviewSerializer


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Booking, Payment
from .services import ChapaService
import uuid


@api_view(['POST'])
@permission_classes([AllowAny])  # Temporarily public for testing
def initiate_payment(request, booking_id):
    """
    Initiate a payment using Chapa.
    In production, change permission to IsAuthenticated.
    """

    # Retrieve booking by ID (no user filter since AllowAny)
    booking = get_object_or_404(Booking, id=booking_id)

    # Prevent duplicate payments
    existing_payment = Payment.objects.filter(
        booking=booking,
        status__in=['pending', 'completed']
    ).first()

    if existing_payment:
        return Response(
            {"error": "A payment already exists for this booking."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Generate unique transaction reference
    tx_ref = f"booking-{booking.id}-{uuid.uuid4()}"

    # Get user info safely
    user = getattr(booking, "user", None)
    email = user.email if user else "guest@example.com"
    first_name = getattr(user, "first_name", "Guest")
    last_name = getattr(user, "last_name", "User")

    # Build callback and return URLs
    callback_url = request.build_absolute_uri('/api/payments/callback/')
    return_url = request.build_absolute_uri(f'/bookings/{booking.id}/payment-status/')

    # Initialize payment with Chapa
    chapa_service = ChapaService()
    chapa_response = chapa_service.initialize_payment(
        amount=booking.total_price,
        email=email,
        first_name=first_name,
        last_name=last_name,
        tx_ref=tx_ref,
        callback_url=callback_url,
        return_url=return_url
    )

    # Validate Chapa response
    if not chapa_response or chapa_response.get('status') != 'success':
        return Response(
            {
                "error": "Failed to initialize payment",
                "details": chapa_response
            },
            status=status.HTTP_502_BAD_GATEWAY
        )

    # Safely get Chapa reference and checkout URL
    data = chapa_response.get('data', {})
    chapa_ref = data.get('tx_ref') or data.get('reference')
    checkout_url = data.get('checkout_url')

    # Create a payment record
    payment = Payment.objects.create(
        booking=booking,
        amount=booking.total_price,
        transaction_id=tx_ref,
        chapa_reference=chapa_ref,
        status='pending',
        chapa_response=chapa_response
    )

    return Response(
        {
            "message": "Payment initialized successfully.",
            "payment_url": checkout_url,
            "transaction_id": tx_ref,
        },
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])  # Temporarily public for testing
def verify_payment(request, transaction_id):
    """
    Verify payment status using Chapa's API.
    In production, switch to IsAuthenticated.
    """

    # Get local payment record
    payment = get_object_or_404(Payment, transaction_id=transaction_id)

    chapa_service = ChapaService()
    verification_response = chapa_service.verify_payment(transaction_id)

    if not verification_response:
        return Response(
            {"error": "Failed to verify payment."},
            status=status.HTTP_502_BAD_GATEWAY
        )

    # Handle verification result
    if verification_response.get('status') == 'success':
        payment_data = verification_response.get('data', {})
        payment_status = payment_data.get('status')

        if payment_status == 'success':
            payment.status = 'completed'
            payment.booking.status = 'confirmed'
            payment.booking.save()

            # This is the critical addition - trigger the email task
            # We do this AFTER saving the booking to ensure the database
            # reflects the confirmed status before the email goes out
            # The delay() method hands this off to Celery without waiting

            message = "Payment verified and booking confirmed."
        else:
            payment.status = 'failed'
            message = "Payment verification returned as failed."

        # Update stored response and save
        payment.chapa_response = verification_response
        payment.save()

        return Response(
            {
                "status": payment.status,
                "message": message,
                "details": payment_data,
            },
            status=status.HTTP_200_OK
        )

    return Response(
        {
            "error": "Payment verification failed.",
            "details": verification_response,
        },
        status=status.HTTP_400_BAD_REQUEST
    )
