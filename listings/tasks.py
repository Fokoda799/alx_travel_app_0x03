# listings/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_booking_confirmation_email(booking_id, user_email, listing_title, check_in, check_out, payment_amount=None):
    """
    Send a booking confirmation email to the user.
    
    The @shared_task decorator tells Celery this function should be
    available as an asynchronous task across your entire project.
    
    We pass individual parameters rather than the entire booking object
    because Celery needs to serialize the data to send it to workers,
    and Django model instances don't serialize well.
    """
    
    subject = f'Booking Confirmation - {listing_title}'

    payment_info = f"\n    - Amount Paid: {payment_amount}" if payment_amount else ""
    
    # Create a nicely formatted email message
    message = f"""
      Dear Valued Customer,
      
      Great news! Your payment has been successfully processed and your booking is confirmed.
      
      Booking Details:
      - Booking ID: {booking_id}
      - Property: {listing_title}
      - Check-in Date: {check_in}
      - Check-out Date: {check_out}{payment_info}
      
      Your reservation is now secured. We've charged your payment method and you're all set for your stay.
      
      If you have any questions or need to make changes to your booking, please don't hesitate to contact us.
      
      We look forward to hosting you!
      
      Best regards,
      ALX Travel App Team
      
      ---
      This is an automated confirmation email. Please keep it for your records.
    """
    
    # Send the email
    # This returns the number of successfully sent emails
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,  # Raise exceptions if sending fails
        )
        return f"Email sent successfully to {user_email}"
    except Exception as e:
        # If email sending fails, Celery will know the task failed
        raise Exception(f"Failed to send email: {str(e)}")
